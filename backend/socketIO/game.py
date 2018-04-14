#!/usr/bin/env python
from models import *
from app import Session,socketio, socketIOClients,turnTimers
from flask_socketio import emit
from flask import request
import sys
import time
from constants import ROUND_KILLER,ALL_GUESSERS,WITHOUT_GAME_CHANGERS

def print_item(item,message):
    print("#################################")
    print("#{} : {}".format(message,item))
    print("#################################")

# request_games: returns a list of current and open games on the server
#  list is in the form [{game1info},{game2info},...,{}]
# client must emit on the /io/game namespace:
#  'request_games'
@socketio.on('request_games',namespace='/io/game')
def request_games():
    session = Session()
    games = GameModel.getAllGames(session)
    gDict = dict()
    for game in games:
        maxPlayersPerTeam = game.maxPlayersPerTeam
        otDict = dict()
        tGame = dict()
        tGame['id'] = game.id
        tGame['gameID'] = game.id
        tGame['name'] = game.name
        tGame['teams'] = list()
        for team in game.teams:
            playerCount = len(team.players)
            tData = {'name':team.name,'id':team.id,'visible':True,'playerCount': playerCount,'maxPlayers':maxPlayersPerTeam}
            if(game.maxPlayersPerTeam <= len(team.players)):
                tData['disableTeamJoin']=True
            otDict[team.id] = tData
        tGame['teams'] = otDict
        gDict[game.id] = tGame
    print_item(gDict,"List of games")
    emit('game_list',gDict)
    session.close()

# validate_game: returns an object that indicates if the game is valid or not.
#  in the form { valid : false }
# client must emit on the /io/game namespace:
#  'validate_game'
@socketio.on('validate_game_config',namespace='/io/game')
def validate_game(data):
    # TODO: returns if the game is valid or not.
    # emits only to the requesting client.
    if(data['_gameValid']):
        data['valid']=True
        print_item(data,'Game config: ')
        emit('show_game_init_button_enabled',data)
    else:
        data['valid']=False
        emit('show_game_init_button_enabled',data)

# init_game: once a game is validated, a client should be able to transmit an init_game.
#  once this has happened and the game has been inited in the db,
#  the socket server will have to emit a response on the views channel
#  which tells the game creator's view to switch to the start game view.
#  At this point the game should become visible to all other clients.
#  clients who join get the waiting for game view.
@socketio.on('init_game',namespace='/io/game')
def init_game(data):
    # TODO: gets passed if the game is valid and tbe user has pressed the init game button
    #  time to build the game in the db and tell the creator's view to switch
    # ...
    # print("Email:======================" + socketIOClients[request.sid].email)
    # if not PlayerModel.is_logged_in():
    #     print ("You are not logged in")
    # else:
    #     initiator = PlayerModel.find_player_by_id(session, 1)
    # print ("The new game: " + str(data))
    session = Session()
    # feedback is a dictionary with 'valid' : boolean, 'message' : error message
    feedback = GameModel.isValidGame(session, data)
    if not feedback['valid']:
        # inform the creator of the game error
        errorMessage = feedback['message']
        return
    initiator = PlayerModel.findPlayerByEmail(session, socketIOClients[request.sid]) #socketIOClients[request.sid].id
    print_item(initiator,"Initiator is: ")
    gameArgs = {k:v for(k,v) in data.items() if k in ['name','turnDuration','numberOfTeams','maxPlayersPerTeam','pointsToWin','skipPenaltyAfter','withGameChangers'] }
    gameArgs['initiator'] = initiator
    game = GameModel(**gameArgs)
    initiatorTeamName = data['initiatorTeam']['name']
    maxPlayersPerTeam=game.maxPlayersPerTeam

    session.add(game)
    session.commit()

    gDict = dict()
    otData = dict()
    returnTeams = []
    for idx,teamObj in enumerate(data['teamData']):
        tData = dict()
        teamName = teamObj['name']

        team = TeamModel(name=teamName,maxPlayersPerTeam=maxPlayersPerTeam)
        game.addTeam(team)
        session.commit()

        if(teamName == initiatorTeamName):
            team.addPlayer(initiator)

        tData['name'] = teamObj['name']
        tData['id'] = team.id
        tData['gameID'] = team.id
        tData['visible'] = True
        tData['playerCount'] = len(team.players)
        tData['maxPlayers'] = game.maxPlayersPerTeam
        otData[team.id] = tData

    gDict[game.id] = {'name' : game.name, 'id' : game.id, 'gameID': game.id , 'teams' : otData }

    viewData = {'swapView':'gameinitiatorwait'}
    emit('created_game',gDict,broadcast=True)
    emit('created_your_game',gDict[game.id])
    emit('swap_view',viewData,namespace="/io/view")
    session.commit()
    session.close()


@socketio.on('join_team',namespace='/io/game')
def join_team(data):
    # Join player to team. Check the game
    session = Session()
    print_item(data,"Join Team: ")
    gameID = data['gameID']
    teamID = data['teamID']
    playerEmail = data['player']
    game = GameModel.getGameById(gameID,session)
    initiator = game.initiator
    player = PlayerModel.findPlayerByEmail(session,playerEmail)

    gData = {
        'id': game.id,
        'gameID': game.id,
        'teams' : dict()
    }
    for team in game.teams:
        # check if all teams have requisite 2 players.
        if(team.id == teamID):
            team.addPlayer(player)
            gData['teams'][team.id] = {
                'id': team.id,
                'name': team.name
            }
            emit('swap_view',{'swapView':'gameplayerwait'},namespace='/io/view')
            emit('joined_team',gData,namespace='/io/game')
            session.commit()
            session.close()
            break

    validate_game_start(data)
# 'validate_game_start': once a game is in a waiting state, joining clients should emit
#  this message.  If the game is indeed ready to start, the server should emit to the starting
#  client that the game is ready to start and the the start game button should become clickable.
@socketio.on('validate_game_start',namespace='/io/game')
def validate_game_start(data):
    session = Session()
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    initiator = game.initiator
    initiatorEmail = initiator.email

    # gData = {'id':'name':}
    ogData = dict()
    gData = {
        'id' : game.id,
        'gameID' : game.id,
        'teams' : dict()
    }
    for team in game.teams:
        tData = {
            'name' : team.name,
            'id' : team.id,
            'visible' : True,
            'playerCount': team.numPlayers(),
            'maxPlayers': game.maxPlayersPerTeam,
            'disableTeamJoin': team.teamFull()
        }
        gData['teams'][team.id] = tData
        ogData[game.id] = gData
        emit('players_on_team',ogData,broadcast=True)
    if(game.readyToStart()):
        emit('show_game_start_button_enabled',room=socketIOClients[initiatorEmail],namespace='/io/view')

    session.close()

# Listens for a start game event from clients.
#  this should only be possible when a game configuration is valid.
#
@socketio.on('start_game',namespace='/io/game')
def start_game(data):
    session = Session()
    print_item(data,'data item to start_game')
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    # Puts the game in started state
    game.setStateStart()
    session.commit()
    emit('game_started',{ 'gameID':game.id },broadcast=True)
    session.close()
    start_new_turn(data)

def start_new_turn(data):
    session = Session()
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    session.commit()
    turn = game.createTurn()
    turnID = turn.id

    session.commit()
    session.close()

    # This happens before the roll.
    setup_turn_roles(gameID)
    # TODO: This happens before the die is rolled. All players should just see views as though things have not been modified.
    setup_turn_views(turnID)


def setup_turn_views(turnID,skipRoll=False):
    session = Session()
    turn = TurnModel.getTurnById(turnID,session)

    moderator   = turn.getModerator()
    teller      = turn.getTeller()
    observers   = turn.getObservers()
    guessers    = turn.getGuessers()

    if(skipRoll):
        emit('swap_view',{ 'swapView' : 'teller' },room=socketIOClients[teller.email],namespace='/io/view')
    else:
        emit('swap_view',{ 'swapView' : 'tellerrolldie' },room=socketIOClients[teller.email],namespace='/io/view')
    emit('swap_view',{ 'swapView' : 'moderator' },room=socketIOClients[moderator.email],namespace='/io/view')

    for guesser in guessers:
        emit('swap_view',{'swapView':'gameplayerturn'},room=socketIOClients[guesser.email],namespace='/io/view')
    for observer in observers:
        emit('swap_view',{'swapView':'gameplayerturn'},room=socketIOClients[observer.email],namespace='/io/view')

    session.commit()
    session.close()


def setup_turn_roles(gameID,gameChanger=-1):
    session = Session()
    game = GameModel.getGameById(gameID,session)
    players = game.getAllPlayers()
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()

    moderator = turn.getModerator()
    teller = turn.getTeller()
    observers = turn.getObservers()
    guessers = turn.getGuessers()

    teamOnDeck = turn.team

    teams = []

    if(not(gameChanger==-1) and gameChanger.gameChangerId == ALL_GUESSERS):
        for team in game.teams:
            tDict = dict()
            tDict['name'] = team.name
            tDict['id'] = team.id
            tDict['teamID'] = team.id
            if(team.id == teamOnDeck.id):
                tDict['onDeck'] = True
            else:
                tDict['onDeck'] = False
            teams.append(tDict)
    else:
        tDict = dict()
        tDict['name'] = teamOnDeck.name
        tDict['id'] = teamOnDeck.id
        tDict['teamID'] = teamOnDeck.id
        tDict['onDeck'] = True
        teams.append(tDict)

    turnRolesData = {
        'teller': {'email': teller.email,'nickname':teller.nickname},
        'moderator':{'email': moderator.email,'nickname':moderator.nickname},
        'observers':[{'email': observer.email,'nickname':observer.nickname} for observer in observers ],
        'guessers': [{'email': guesser.email,'nickname': guesser.nickname} for guesser in guessers ]
    }
    players = game.getAllPlayers()
    turnData = {
        'roles': turnRolesData,
        'team' : {
            'name': teamOnDeck.name,
            'id': teamOnDeck.id,
            'teamID': teamOnDeck.id,
            'turnID': turn.id
        },
        'teams': teams,
    }
    for player in players:
        emit('turn_data',turnData,room=socketIOClients[player.email],namespace='/io/game')
    for observer in observers:
        emit('turn_role_assignment',{ 'role' : 'observer' },room=socketIOClients[observer.email],namespace='/io/game')
    for guesser in guessers:
        emit('turn_role_assignment',{ 'role' : 'guesser' },room=socketIOClients[guesser.email],namespace='/io/game')

@socketio.on('roll_wheel',namespace='/io/game')
def roll_wheel(data):
    session = Session()
    gameID = data['gameID']
    duration = data['duration']
    print_item(data,"Rolling wheel: ")
    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()
    gameChanger = turn.setGameChanger()
    rollWheel = {
        'gameID' : gameID,
        'rollID' : gameChanger.gameChangerId,
        'description' : gameChanger.description,
        'name': gameChanger.name
    }
    emit('my_roll_result',rollWheel)
    time.sleep(duration + 1.5)
    emit('enable_start_turn_button')
    session.commit()
    session.close()

@socketio.on('starting_turn',namespace='/io/game')
def start_turn(data):
    session = Session()
    gameID = data['gameID']

    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()

    moderator = turn.getModerator()
    teller = turn.getTeller()
    gameChanger = turn.getGameChanger()
    rollWheel = {
        'gameID' : gameID,
        'rollID' : gameChanger.gameChangerId,
        'description' : gameChanger.description,
        'name': gameChanger.name
    }

    if( gameChanger.gameChangerId == ALL_GUESSERS):
        setup_turn_roles(gameID,gameChanger)

    if( gameChanger.gameChangerId == ROUND_KILLER ):
        start_new_turn(data)
        session.commit()
        session.close()
        return

    players = game.getAllPlayers()
    for player in players:
        emit('roll_result',rollWheel,room=socketIOClients[player.email],namespace='/io/game')


    cardData = turn.loadCard()
    cardData['showCard'] = True
    emit('swap_view',{'swapView':'teller'},room=socketIOClients[teller.email],namespace='/io/view')
    time.sleep(1)

    emit('load_card',cardData,room=socketIOClients[teller.email],namespace='/io/card')
    emit('load_card',cardData,room=socketIOClients[moderator.email],namespace='/io/card')
    turn.startTimer(timer_notify_turn_complete)

    session.commit()
    session.close()

@socketio.on('load_next_card',namespace='/io/game')
def load_next_card(data):
    session = Session()
    gameID = data['gameID']

    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()

    moderator = turn.getModerator()
    teller = turn.getTeller()
    cardData = turn.loadCard()
    cardData['showCard'] = True
    emit('load_card',cardData,room=socketIOClients[teller.email],namespace='/io/card')
    emit('load_card',cardData,room=socketIOClients[moderator.email],namespace='/io/card')
    session.commit()
    session.close()

@socketio.on("pause_timer",namespace="/io/timer")
def pause_timer(data):
    session = Session()
    print_item(data,"PAUSING TIMER")
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    session.commit()
    turn = round.getCurrentTurn()
    turnID = turn.id
    timer = turnTimers[turnID]
    timer.pause()
    session.close()


@socketio.on("resume_timer",namespace="/io/timer")
def resume_timer(data):
    session = Session()
    print_item(data,"RESUMING TIMER")
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()
    turnID = turn.id
    timer = turnTimers[turnID]
    timer.resume()
    session.close()

@socketio.on("timer_notify_turn_complete",namespace="/io/game")
def timer_notify_turn_complete(data):
    session = Session()
    print_item(data,"TURN COMPLETE!!!")
    # TODO: notify clients of turn completion.
    # TODO: emit clear cards.
    # TODO: sleep for a second.
    # TODO: start next turn!
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    players = game.getAllPlayers()
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()
    print_item(turn,"TURN ITEM TO BE REPLACED")
    waitDuration = 3
    for player in players:
        emit('swap_view',{ 'swapView' : 'waitforturn'},room=socketIOClients[player.email],namespace='/io/view')
    time.sleep(waitDuration)
    start_new_turn()

    session.commit()
    session.close()

@socketio.on('award_penalty',namespace="/io/card")
def award_penalty(data):
    session = Session()
    turnID = data['turnID']
    turn =  TurnModel.getTurnById(turnID,session)
    turn.awardTeam()
    session.commit()
    session.close()
    load_next_card(data)

@socketio.on('award_point',namespace="/io/card")
def award_point(data):
    session = Session()
    turnID = data['turnID']
    turn =  TurnModel.getTurnById(turnID,session)
    turn.awardPoint()
    session.commit()
    session.close()
    load_next_card(data)

@socketio.on('skip_card',namespace="/io/card")
def skip_card(data):
    session = Session()
    print_item(data,"SKIP RECEIVED")
    turnID = data['turnID']
    turn =  TurnModel.getTurnById(turnID,session)
    turn.skip()
    session.commit()
    session.close()
    load_next_card(data)
