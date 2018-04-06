from app import engine, Session
from models import Base as AppModelBase
from db import delete_db
from models import CardModel, PlayerModel, TeamModel, GameModel, GameChanger, GameChangers, RoundModel
import random

def testGameCreate():
    session = Session()
    initiator = PlayerModel.findPlayerById(session, 1)
    print ("Email: " + initiator.email)
    game = GameModel(initiator, "CS699", 60)
    team1 = TeamModel("Team 1")
    team2 = TeamModel("Team 2")
    team3 = TeamModel("Team 3")
    team4 = TeamModel("Team 4")
    team5 = TeamModel("Team 5")
    team6 = TeamModel("Team 6")
    team7 = TeamModel("Team 7")
    teams = [team1, team2, team3, team4, team5, team6, team7]
    initiator.team = team1
    session.flush()
    game.teams = teams
    session.add(game)
    session.commit()
    session.close()

def testCreatePlayers():
    session = Session()
    for i in range(50):
        email = "member" + str(i + 1) + "@bsu.edu"
        if PlayerModel.emailExists(session, email):
            print ("the entered email already exists")
        else:
            member1 = PlayerModel("Member " + str(i + 1), email, 3)
            session.add(member1)
            session.flush()
    session.commit()
    session.close()

def testIsLoggedIn():
    if PlayerModel.isLoggedIn():
        print ("is logged in")
    else:
        print ("is not logged in")

def testJoinTeam():
    session = Session()
    for i in range(1, 51):
        playerId = i
        player = PlayerModel.findPlayerById(session, playerId)
        if player is None:
            print("the player does not exist")
            return
        numberOfTeams = 7
        teamId = random.randint(1, numberOfTeams - 1)
        team = TeamModel.getTeamById(session, teamId)
        if team is None:
            print("the team does not exist")
            return
        player.team = team
        session.flush()
    session.commit()
    session.close()

def testSaveCards():
    session = Session()
    for index in range(50):
        forbidden = "{'word1', 'word2', 'word3', 'word4'}"
        card = CardModel("word_" + str(index + 1), forbidden, "Book", "345")
        session.add(card)
        session.flush()
    session.commit()
    session.close()

def testAddUsedCard():
    session = Session()
    game = GameModel.getGameById(session, 1)
    for i in range(5):
        card = CardModel.findCardById(session, i + 1)
        game.addUsedCard(card)
    session.commit()
    session.close()

def testFindUsedCards():
    session = Session()
    game = GameModel.getGameById(session, 1)
    usedCards = game.getUsedCards()
    for card in usedCards:
        print(card.buzzword)
    session.commit()
    session.close()

def testFindUnusedCards():
    session = Session()
    game = GameModel.getGameById(session, 1)
    unusedCards = game.getUnusedCards(session)
    for card in unusedCards:
        print(card.buzzword)
    session.commit()
    session.close()

def testGameChanger():
    gameChangers = GameChangers()
    for i in range(100000):
        selectedGameChanger = gameChangers.rollDie()
        selectedGameChanger.count += 1
    for key, changer in gameChangers.changers.items():
        print("Weight: " + str(changer.weight) + ", Selected: " + str(changer.count))

def testCreateTurn():
    session = Session()
    game = GameModel.getGameById(session, 1)
    game.createTurn()
    session.commit()
    session.close()

def testAddGameChanger():
    session = Session()
    game = GameModel.getGameById(session, 1)
    round = game.getCurrentRound()
    turn = round.getLastTurn()
    turn.setGameChanger()
    turn.updatePlayerRoles(game) # roles have to be updated if the all-guessers game changer is selected
    session.commit()
    session.close()

def testLoadCard():
    session = Session()
    game = GameModel.getGameById(session, 1)
    round = game.getCurrentRound()
    turn = round.getLastTurn()
    card = turn.loadCard(session, game)
    print("buzzword: " + card.buzzword)
    session.commit()
    session.close()

# delete_db(engine)
# AppModelBase.metadata.create_all(engine)
#
# testCreatePlayers()
# testGameCreate()
# testJoinTeam()
# testSaveCards()
# testCreateTurn()
# testAddUsedCard()
# testFindUsedCards()
# testFindUnusedCards()
# testGameChanger()
# test_is_logged_in()
# testAddGameChanger()
testLoadCard()
