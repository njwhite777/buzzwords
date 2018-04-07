#!/usr/bin/env python
from models import *
from app import Session,socketio, socketIOClients
from flask_socketio import emit
from flask import request
import sys


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
    tGlist = list()
    for game in games:
        maxPlayersPerTeam = game.maxPlayersPerTeam
        tGame = dict()
        tGame['id'] = game.id
        tGame['name'] = game.name
        tGame['teams'] = list()
        for team in game.teams:
            playerCount = len(team.players)
            tData = {'name':team.name,'id':team.id,'visible':True,'playerCount': playerCount,'maxPlayers':maxPlayersPerTeam}
            if(game.maxPlayersPerTeam <= len(team.players)):
                tData['disableTeamJoin']=True
            tGame['teams'].append(tData)

        tGlist.append(tGame)
    print_item(tGlist,"List of games")
    emit('game_list',tGlist)
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
    initiator = PlayerModel.findPlayerByEmail(session, socketIOClients[request.sid]) #socketIOClients[request.sid].id
    print_item(initiator,"Initiator is: ")
    gameArgs = {k:v for(k,v) in data.items() if k in ['name','turnDuration','numberOfTeams','maxPlayersPerTeam','pointsToWin','skipPenaltyAfter','withGameChangers'] }
    gameArgs['initiator'] = initiator
    game = GameModel(**gameArgs)
    initiatorTeamName = data['initiatorTeam']['name']
    maxPlayersPerTeam=game.maxPlayersPerTeam

    print_item(data,"game")
    session.add(game)
    session.commit()

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
        tData['visible'] = True
        tData['playerCount'] = len(team.players)
        tData['maxPlayers'] = game.maxPlayersPerTeam
        returnTeams.append(tData)

    returnData = {'name' : game.name, 'id' : game.id, 'teams' : returnTeams }
    session.commit()
    session.close()
    viewData = {'swapView':'gameinitiatorwait'}
    emit('created_game',returnData,broadcast=True)
    emit('created_your_game',returnData)
    emit('swap_view',viewData,namespace="/io/view")


@socketio.on('join_team',namespace='/io/game')
def join_team(data):
    # Join player to team. Check the game
    session = Session()
    print_item(data,"Join Team: ")
    gameID = data['gameID']
    teamID = data['teamID']
    playerEmail = data['player']
    game = GameModel.getGameById(session,gameID)
    initiator = game.initiator
    player = PlayerModel.findPlayerByEmail(session,playerEmail)

    for team in game.teams:
        # check if all teams have requisite 2 players.
        if(team.id == teamID):
            team.addPlayer(player)
            session.commit()
            session.close()
            emit('swap_view',{'swapView':'gameplayerwait'},namespace='/io/view')
            break

    validate_game_start(data)
# 'validate_game_start': once a game is in a waiting state, joining clients should emit
#  this message.  If the game is indeed ready to start, the server should emit to the starting
#  client that the game is ready to start and the the start game button should become clickable.
@socketio.on('validate_game_start',namespace='/io/game')
def validate_game_start(data):
    session = Session()
    gameID = data['gameID']
    game = GameModel.getGameById(session,gameID)
    initiator = game.initiator
    initiatorEmail = initiator.email

    # gData = {'id':'name':}
    for team in game.teams:
        tData = {
            'name' : team.name,
            'id' : team.id,
            'visible' : True,
            'playerCount': team.numPlayers(),
            'maxPlayers': game.maxPlayersPerTeam,
            'disableTeamJoin': team.teamFull()
        }
        emit('players_on_team',tData,broadcast=True)
    if(game.readyToStart()):
        emit('show_game_start_button_enabled',room=socketIOClients[initiatorEmail],namespace='/io/view')

    session.close()

# Listens for a start game event from clients.
#  this should only be possible when a game configuration is valid.
#
@socketio.on('start_game',namespace='/io/game')
def start_game(data):
    session = Session()
    gameID = data['gameID']
    game = GameModel.getGameById(session,gameID)
    # Puts the game in started state
    game.setStateStart()
    session.commit()
    emit('game_started',{ 'gameID':game.id },broadcast=True)
    session.close()
    start_new_turn(data)

def start_new_turn(data):
    session = Session()
    gameID = data['gameID']
    game = GameModel.getGameById(session,gameID)
    turn = game.createTurn(session)
    session.commit()
    moderator = turn.getModerator()
    teller = turn.getTeller()
    observers = turn.getObservers(game)
    guessers = turn.getGuessers(game)
    teamOnDeck = turn.team

    turnRolesData = {
        'teller': {'email': teller.email,'nickname':teller.nickname},
        'moderator':{'email': moderator.email,'nickname':moderator.nickname},
        'observers':[{'email': observer.email,'nickname':observer.nickname} for observer in observers ],
        'guessers': [{'email': guesser.email,'nickname': guesser.nickname} for guesser in guessers ]
    }

    emit('swap_view',{ 'swapView' : 'tellerrolldie' },room=socketIOClients[teller.email],namespace='/io/view')
    # If round modifiers are off, use the following.
    # emit('swap_view',{ 'swapView' : 'teller' },room=socketIOClients[teller.email],namespace='/io/view')
    emit('swap_view',{ 'swapView' : 'moderator' },room=socketIOClients[moderator.email],namespace='/io/view')
    for guesser in guessers:
        emit('swap_view',{'swapView':'guesser'},room=socketIOClients[guesser.email],namespace='/io/view')
    for observer in observers:
        emit('swap_view',{'swapView':'observer'},room=socketIOClients[observer.email],namespace='/io/view')

    players = game.getAllPlayers()
    for player in players:
        print
        emit('turn_roles',turnRolesData,room=socketIOClients[player.email],namespace='/io/game',)

    session.commit()
    session.close()
