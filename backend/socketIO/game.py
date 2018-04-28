#!/usr/bin/env python
from models import *
import globalVars
from flask_socketio import emit
from flask import request
import sys
import time
import globalVars
from constants import ROUND_KILLER,ALL_GUESSERS,WITHOUT_GAME_CHANGERS,GAME_READY

def print_item(item,message):
    print("#################################")
    print("#{} : {}".format(message,item))
    print("#################################")

# request_games: returns a list of current and open games on the server
#  list is in the form [{game1info},{game2info},...,{}]
# client must emit on the /io/game namespace:
#  'request_games'
@globalVars.socketio.on('request_games',namespace='/io/game')
def request_games():
    print("I am requesting!")
    session = globalVars.Session()
    games = GameModel.getAllGames(session,filter=GAME_READY)
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
@globalVars.socketio.on('validate_game_config',namespace='/io/game')
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
@globalVars.socketio.on('init_game',namespace='/io/game')
def init_game(data):
    # TODO: gets passed if the game is valid and tbe user has pressed the init game button
    #  time to build the game in the db and tell the creator's view to switch
    # ...
    # print("Email:======================" + globalVars.socketIOClients[request.sid].email)
    # if not PlayerModel.is_logged_in():
    #     print ("You are not logged in")
    # else:
    #     initiator = PlayerModel.find_player_by_id(session, 1)
    # print ("The new game: " + str(data))
    session = globalVars.Session()
    # feedback is a dictionary with 'valid' : boolean, 'message' : error message
    feedback = GameModel.isValidGame(session, data)
    if not feedback['valid']:
        # inform the creator of the game error
        errorMessage = feedback['message']
        return
    initiator = PlayerModel.findPlayerByEmail(session, globalVars.socketIOClients[request.sid]) #globalVars.socketIOClients[request.sid].id

    gameArgs = {k:v for(k,v) in data.items() if k in ['name','turnDuration','numberOfTeams','maxPlayersPerTeam','pointsToWin','skipPenaltyAfter','withGameChangers'] }
    # TODO: UNDO THIS!!!###############
    gameArgs['turnDuration'] = 5
    gameArgs['pointsToWin'] = 5
    ###################################
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


@globalVars.socketio.on('join_team',namespace='/io/game')
def join_team(data):
    # Join player to team. Check the game
    session = globalVars.Session()
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
@globalVars.socketio.on('validate_game_start',namespace='/io/game')
def validate_game_start(data):
    session = globalVars.Session()
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
        emit('show_game_start_button_enabled',room=globalVars.socketIOClients[initiatorEmail],namespace='/io/view')

    session.close()

# Listens for a start game event from clients.
#  this should only be possible when a game configuration is valid.
#
@globalVars.socketio.on('start_game',namespace='/io/game')
def start_game(data):
    session = globalVars.Session()
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
    session = globalVars.Session()
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    session.commit()
    turn = game.createTurn()
    turnID = turn.id

    session.commit()
    session.close()

    setup_turn_roles(gameID)
    setup_turn_views(turnID)


def setup_turn_views(turnID,skipRoll=False):
    session = globalVars.Session()
    turn = TurnModel.getTurnById(turnID,session)

    moderator   = turn.getModerator()
    teller      = turn.getTeller()
    observers   = turn.getObservers()
    guessers    = turn.getGuessers()

    if(skipRoll):
        globalVars.socketio.emit('swap_view',{ 'swapView' : 'teller' },room=globalVars.socketIOClients[teller.email],namespace='/io/view')
    else:
        globalVars.socketio.emit('swap_view',{ 'swapView' : 'tellerrolldie' },room=globalVars.socketIOClients[teller.email],namespace='/io/view')
    globalVars.socketio.emit('swap_view',{ 'swapView' : 'moderator' },room=globalVars.socketIOClients[moderator.email],namespace='/io/view')

    for guesser in guessers:
        globalVars.socketio.emit('swap_view',{'swapView':'gameplayerturn'},room=globalVars.socketIOClients[guesser.email],namespace='/io/view')
    for observer in observers:
        globalVars.socketio.emit('swap_view',{'swapView':'gameplayerturn'},room=globalVars.socketIOClients[observer.email],namespace='/io/view')

    session.commit()
    session.close()


def setup_turn_roles(gameID,gameChanger=-1):
    session = globalVars.Session()
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
        globalVars.socketio.emit('turn_data',turnData,room=globalVars.socketIOClients[player.email],namespace='/io/game')
    for observer in observers:
        globalVars.socketio.emit('turn_role_assignment',{ 'role' : 'observer' },room=globalVars.socketIOClients[observer.email],namespace='/io/game')
    for guesser in guessers:
        globalVars.socketio.emit('turn_role_assignment',{ 'role' : 'guesser' },room=globalVars.socketIOClients[guesser.email],namespace='/io/game')

@globalVars.socketio.on('roll_wheel',namespace='/io/game')
def roll_wheel(data):
    session = globalVars.Session()
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
    print_item(rollWheel,"ROLL RESULT WAS")
    emit('my_roll_result',rollWheel)

    globalVars.socketio.sleep(duration + 1.5)
    emit('enable_start_turn_button')
    session.commit()
    session.close()

@globalVars.socketio.on('starting_turn',namespace='/io/game')
def start_turn(data):
    session = globalVars.Session()
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
    players = game.getAllPlayers()

    if( gameChanger.gameChangerId == ALL_GUESSERS):
        setup_turn_roles(gameID,gameChanger)

    if( gameChanger.gameChangerId == ROUND_KILLER ):

        if(game.isGameOver()):
            for player in players:
                emit('swap_view',{ 'swapView' : 'endgame'},room=globalVars.socketIOClients[player.email],namespace='/io/view')
            session.commit()
            session.close()
            return

        start_new_turn(data)
        session.commit()
        session.close()
        return


    for player in players:
        emit('roll_result',rollWheel,room=globalVars.socketIOClients[player.email],namespace='/io/game')
        emit('turn_started',{ 'turnID' : turn.id },room=globalVars.socketIOClients[player.email],namespace='/io/game')

    cardData = turn.loadCard()
    print_item(cardData,"CURRENT CARD IS")
    cardData['showCard'] = True
    emit('swap_view',{'swapView':'teller'},room=globalVars.socketIOClients[teller.email],namespace='/io/view')
    globalVars.socketio.sleep(1)

    emit('load_card',cardData,room=globalVars.socketIOClients[teller.email],namespace='/io/card')
    emit('load_card',cardData,room=globalVars.socketIOClients[moderator.email],namespace='/io/card')

    if (cardData['card']['isPhrase']==1):
        isPhrase = "True"
    else:
        isPhrase = "False"

    for player in players:

        emit('is_phrase',{ 'isPhrase': isPhrase },room=globalVars.socketIOClients[player.email],namespace='/io/game')

    turn.startTimer()
    session.commit()
    session.close()

@globalVars.socketio.on('load_next_card',namespace='/io/game')
def load_next_card(data):
    session = globalVars.Session()
    gameID = data['gameID']

    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()

    moderator = turn.getModerator()
    teller = turn.getTeller()
    cardData = turn.loadCard()
    cardData['showCard'] = True
    emit('load_card',cardData,room=globalVars.socketIOClients[teller.email],namespace='/io/card')
    emit('load_card',cardData,room=globalVars.socketIOClients[moderator.email],namespace='/io/card')

    if (cardData['card']['isPhrase']==1):
        isPhrase = "True"
    else:
        isPhrase = "False"

    for player in players:
        emit('is_phrase',{ 'isPhrase': isPhrase },room=globalVars.socketIOClients[player.email],namespace='/io/game')

    session.commit()
    session.close()

@globalVars.socketio.on("pause_timer",namespace="/io/timer")
def pause_timer(data):
    session = globalVars.Session()
    print_item(data,"PAUSING TIMER")
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    session.commit()
    turn = round.getCurrentTurn()
    turnID = turn.id
    timer = globalVars.turnTimers[turnID]
    timer.pause()
    session.close()


@globalVars.socketio.on("resume_timer",namespace="/io/timer")
def resume_timer(data):
    session = globalVars.Session()
    print_item(data,"RESUMING TIMER")
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()
    turnID = turn.id
    timer = globalVars.turnTimers[turnID]
    timer.resume()
    session.close()

@globalVars.socketio.on("turn_complete",namespace="/io/game")
def turn_complete(data):
    session = globalVars.Session()
    # TODO: notify clients of turn completion
    # TODO: sleep for a second.
    # TODO: start next turn!
    gameID = data['gameID']
    game = GameModel.getGameById(gameID,session)
    players = game.getAllPlayers()
    round = game.getCurrentRound()
    turn = round.getCurrentTurn()
    teamScoreData = turn.getAllTeamScores()

    print_item(game,"CHECKING Game.isGameOver()")
    if(game.isGameOver()):
        for player in players:
            globalVars.socketio.emit('swap_view',{ 'swapView' : 'endgame'},room=globalVars.socketIOClients[player.email],namespace='/io/view')
        session.commit()
        session.close()
        return

    waitDuration = 2
    for player in players:
        # TODO: ADD SCORE INFO TO turn_finished
        globalVars.socketio.emit('turn_finished',{ 'turnID' : turn.id },room=globalVars.socketIOClients[player.email],namespace='/io/game')
        globalVars.socketio.emit('report_score',teamScoreData,room=globalVars.socketIOClients[player.email],namespace='/io/game')
        globalVars.socketio.emit('swap_view',{ 'swapView' : 'waitforturn'},room=globalVars.socketIOClients[player.email],namespace='/io/view')

    timer = globalVars.turnTimers[turn.id]
    print(timer)
    del globalVars.turnTimers[turn.id]
    globalVars.socketio.sleep(waitDuration)
    start_new_turn(data)

    session.commit()
    session.close()

@globalVars.socketio.on('award_penalty',namespace="/io/card")
def award_penalty(data):
    session = globalVars.Session()
    print_item(data,"TAKE POINT RECEIVED")
    turnID = data['turnID']
    turn =  TurnModel.getTurnById(turnID,session)
    turn.penaliseTeam()
    session.commit()
    session.close()
    load_next_card(data)

@globalVars.socketio.on('award_point',namespace="/io/card")
def award_point(data):
    session = globalVars.Session()
    turnID = data['turnID']
    teamID = data['teamID']
    turn =  TurnModel.getTurnById(turnID,session)
    turn.awardTeamByID(teamID)
    session.commit()
    session.close()
    load_next_card(data)

@globalVars.socketio.on('skip_card',namespace="/io/card")
def skip_card(data):
    session = globalVars.Session()
    print_item(data,"SKIP RECEIVED")
    turnID = data['turnID']
    turn =  TurnModel.getTurnById(turnID,session)
    turn.skip()
    session.commit()
    session.close()
    load_next_card(data)
