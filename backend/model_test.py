from app import engine, Session
from models import Base as AppModelBase
from db import delete_db
from models import CardModel, PlayerModel, TeamModel, GameModel, GameChanger, GameChangers

def test_game_create():
    session = Session()
    initiator = PlayerModel.find_player_by_id(session, 1)
    print ("Email: " + initiator.email)
    game = GameModel("CS699", initiator, 60)
    team1 = TeamModel("Team 1")
    team2 = TeamModel("Team 2")
    teams = [team1, team2]
    initiator.team = team1
    session.commit()
    game.set_teams(teams)
    initiator.game = game
    session.add(game)
    session.commit()
    session.close()

def test_create_player():
    session = Session()
    email = "member3@yahoo.com"
    if PlayerModel.email_exists(session, email):
        print ("the entered email already exists")
    else:
        member1 = PlayerModel("Member 3", email, 3)
        #member2 = PlayerModel("Member 2", "member2@yahoo.com", 3)
        session.add(member1)
        session.commit()
        print ("account created")
    session.close()

def test_is_logged_in():
    if PlayerModel.is_logged_in():
        print ("is logged in")
    else:
        print ("is not logged in")

def test_join_team():
    session = Session()
    player_id = 3 # should come from the http session
    player = PlayerModel.find_player_by_id(session, player_id)
    if player is None:
        print("the player does not exist")
        return
    team_id = 1 # should come from the client
    team = TeamModel.find_team_by_id(session, team_id)
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

def test_add_used_card():
    session = Session()
    game = GameModel.get_game_by_id(session, 1)
    for i in range(5):
        card = CardModel.find_card_by_id(session, i + 1)
        game.add_used_card(card)
    session.commit()
    session.close()

def test_find_used_cards():
    session = Session()
    game = GameModel.get_game_by_id(session, 1)
    used_cards = game.get_used_cards()
    for card in used_cards:
        print(card.buzzword)
    session.commit()
    session.close()

def test_find_unused_cards():
    session = Session()
    game = GameModel.get_game_by_id(session, 1)
    unused_cards = game.get_unused_cards(session)
    for card in unused_cards:
        print(card.buzzword)
    session.commit()
    session.close()

def testGameChanger():
    gameChangers = GameChangers()
    selectedGameChanger = gameChangers.rollDie()
    print(selectedGameChanger.description)





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
