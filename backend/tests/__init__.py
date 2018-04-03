#!/usr/bin/python
from models import GameModel,PlayerModel,TeamModel
from app import GAME_READY

def start_game_db(Session):

    session = Session()

    players = list()
    players.append(PlayerModel(nickname='nwhite',email='njwhite777@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite2',email='njwhite7772@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite4',email='njwhite7774@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite3',email='njwhite7773@gmail.com',role=4))

    numberOfTeams=2
    minRequiredPlayers=2
    game = GameModel(name='game1',initiator=players[0],numberOfTeams=numberOfTeams,minRequiredPlayers=minRequiredPlayers)

    session.add(game)
    session.commit()

    for i in range(numberOfTeams):
        teamName = 'team'+str(i)
        team=TeamModel(teamName)

        if(i == 0):
            team.add_player(players[0])
            team.add_player(players[1])
        else:
            team.add_player(players[2])
            team.add_player(players[3])

        game.add_team(team)
    game.gameState = GAME_READY

    session.commit()
    session.close()
