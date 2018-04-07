#!/usr/bin/python
from models import GameModel,PlayerModel,TeamModel,CardModel
from constants import GAME_READY

def start_game2_db(Session):
    session = Session()

    players = list()
    players.append(PlayerModel(nickname='nwhite',email='njwhite777@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite2',email='njwhite7772@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite3',email='njwhite7773@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite4',email='njwhite7774@gmail.com',role=4))



    numberOfTeams=2
    minRequiredPlayers=2
    maxPlayersPerTeam=2
    game = GameModel(name='game1',initiator=players[0],numberOfTeams=numberOfTeams,minRequiredPlayers=minRequiredPlayers,maxPlayersPerTeam=maxPlayersPerTeam)



    session.add(game)
    session.commit()

    for i in range(numberOfTeams):
        teamName = 'team'+str(i)
        team=TeamModel(teamName)

        if(i == 0):
            team.addPlayer(players[0])
            team.addPlayer(players[1])
        else:
            team.addPlayer(players[2])
            team.addPlayer(players[3])

        game.addTeam(team)
    game.gameState = GAME_READY

    session.commit()
    session.close()


def start_game_db(Session):

    session = Session()

    players = list()
    players.append(PlayerModel(nickname='nwhite',email='njwhite777@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite2',email='njwhite7772@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite3',email='njwhite7773@gmail.com',role=4))
    players.append(PlayerModel(nickname='nwhite4',email='njwhite7774@gmail.com',role=4))

    numberOfTeams=2
    minRequiredPlayers=2
    maxPlayersPerTeam=2
    game = GameModel(name='game1',initiator=players[0],numberOfTeams=numberOfTeams,minRequiredPlayers=minRequiredPlayers,maxPlayersPerTeam=maxPlayersPerTeam)

    for index in range(50):
        print("Putting card.")
        forbidden = "{'word1', 'word2', 'word3', 'word4'}"
        card = CardModel("word_" + str(index + 1), forbidden, "Book", "345")
        session.add(card)

    session.add(game)
    session.commit()

    for i in range(numberOfTeams):
        teamName = 'team'+str(i)
        team=TeamModel(teamName)

        if(i == 0):
            team.addPlayer(players[0])
            team.addPlayer(players[1])
        else:
            team.addPlayer(players[2])
            team.addPlayer(players[3])

        game.addTeam(team)
    game.gameState = GAME_READY

    session.commit()
    session.close()
