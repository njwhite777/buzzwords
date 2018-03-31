from app import engine, session
from models import Base as AppModelBase
from db import delete_db
from models import CardModel, PlayerModel, TeamModel, GameModel

def test_game_create():
    initiator = PlayerModel.find_player_by_id(session, 1)
    print (initiator)
    game = GameModel("CS699", initiator, 60)
    team1 = TeamModel("Team 1")
    team2 = TeamModel("Team 2")
    teams = [team1, team2]
    # team1.add_member(initiator)
    # session.commit()
    game.set_teams(teams)
    initiator.game = game
    session.add(game)
    session.commit()

def test_create_player():
    email = "member1@yahoo.com"
    if PlayerModel.email_exists(session, email):
        print ("the entered email already exists")
    else:
        member1 = PlayerModel("Member 1", email, 3)
        #member2 = PlayerModel("Member 2", "member2@yahoo.com", 3)
        session.add(member1)
        session.commit()
        print ("account created")

def test_is_logged_in():
    if PlayerModel.is_logged_in():
        print ("is logged in")
    else:
        print ("is not logged in")

#delete_db(engine)
#AppModelBase.metadata.create_all(engine)

# test_is_logged_in()
#test_create_player()
test_game_create()
