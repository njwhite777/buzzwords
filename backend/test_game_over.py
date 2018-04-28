#!/usr/bin/env python
from app import create_app,create_db_connection,getQuizletCards
from flask_socketio import SocketIO
import globalVars
from models import *

environment = 'dev'
app = create_app(app_name="buzzwords",environment=environment,configFile={ 'dev_config' : 'settings','prod_config':''},config={})
globalVars.socketio=SocketIO(app)
globalVars.Session,globalVars.engine = create_db_connection(app,rebuilddb=True)
session = globalVars.Session()
if(environment):
    getQuizletCards()


for i in range(50):
    email = "member" + str(i + 1) + "@bsu.edu"
    if PlayerModel.emailExists(session, email):
        print ("the entered email already exists")
    else:
        member1 = PlayerModel("Member " + str(i + 1), email, 3)
        session.add(member1)
        session.flush()
session.commit()

initiator = PlayerModel.findPlayerById(session, 1)
#print ("Email: " + initiator.email)
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

for i in range(1,50):
    team = TeamModel.getTeamById(session, (i % 7) + 1)
    player = PlayerModel.findPlayerById(session, i)
    player.team = team
    session.flush()
    session.commit()

print("READING THE GAME>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
game = GameModel.getGameById(1, session)

print("CREATING TURN>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
turn = game.createTurn()
print("DONE CREATING TURN>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
turn.setGameChanger()

print("ANOTHER CREATING TURN>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
turn = game.createTurn()
print("DONE ANOTHER CREATING TURN>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
turn.setGameChanger()
print("LOADING A CARD>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print("the card>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", turn.loadCard())
print("DONE LOADING A CARD>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
session.commit()



print("hasAtLeastOneRound>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", game.hasAtLeastOneRound(session))
print("teamsHaveEqualTurns>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", game.teamsHaveEqualTurns())
print("teamHasReachedThreshold>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", game.teamHasReachedThreshold())
print("isGameOver>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", game.isGameOver())
session.close()
