from app import engine, Session
from models import Base as AppModelBase
from db import delete_db
from models import CardModel, PlayerModel, TeamModel, GameModel, GameChanger, GameChangers

def testGameCreate():
    session = Session()
    initiator = PlayerModel.findPlayerById(session, 1)
    print ("Email: " + initiator.email)
    game = GameModel("CS699", initiator, 60)
    team1 = TeamModel("Team 1")
    team2 = TeamModel("Team 2")
    teams = [team1, team2]
    initiator.team = team1
    session.commit()
    game.setTeams(teams)
    initiator.game = game
    session.add(game)
    session.commit()
    session.close()

def testCreatePlayer():
    session = Session()
    email = "member3@yahoo.com"
    if PlayerModel.emailExists(session, email):
        print ("the entered email already exists")
    else:
        member1 = PlayerModel("Member 3", email, 3)
        #member2 = PlayerModel("Member 2", "member2@yahoo.com", 3)
        session.add(member1)
        session.commit()
        print ("account created")
    session.close()

def testIsLoggedIn():
    if PlayerModel.isLoggedIn():
        print ("is logged in")
    else:
        print ("is not logged in")

def testJoinTeam():
    session = Session()
    playerId = 3 # should come from the http session
    player = PlayerModel.findPlayerById(session, playerId)
    if player is None:
        print("the player does not exist")
        return
    teamId = 1 # should come from the client
    team = TeamModel.findTeamById(session, teamId)
    if team is None:
        print("the team does not exist")
        return
    player.team = team
    session.commit()
    session.close()

def test_save_cards():
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
    #print(selectedGameChanger.description)





#delete_db(engine)
#AppModelBase.metadata.create_all(engine)

#test_is_logged_in()
#test_create_player()
#test_game_create()
#test_join_team()
#test_save_cards()
#test_add_used_card()
#test_find_used_cards()
# test_find_unused_cards()
testGameChanger()
