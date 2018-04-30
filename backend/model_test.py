from app import engine, Session
from models import Base as AppModelBase
from db import delete_db
from models import CardModel, PlayerModel, TeamModel, GameModel, GameChanger, GameChangers, RoundModel
import random
import unittest
from constants import *

class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test1CreatePlayers(self):
        delete_db(engine)
        AppModelBase.metadata.create_all(engine)
        for i in range(50):
            email = "member" + str(i + 1) + "@bsu.edu"
            if PlayerModel.emailExists(self.session, email):
                print ("the entered email already exists")
            else:
                member1 = PlayerModel("Member " + str(i + 1), email, 3)
                self.session.add(member1)
                self.session.flush()
        self.session.commit()
        self.assertEqual(PlayerModel.numberOfRows(self.session),50)

        print("\n\n*************Test add exist Player**********************\n\n")
        member2_email = "member2@bsu.edu"
        if(PlayerModel.emailExists(self.session, member2_email)):
            print ("the entered email already exists")
        else:
            member2 = PlayerModel("Member2", "member2@bsu.edu",3)
            self.session.add(member2)
            self.session.flush()
            self.session.commit()
        self.assertEqual(PlayerModel.numberOfRows(self.session),50)

        print("\n\n*************Test add invalid email Player***************\n\n")
        member3_email = ""
        member3_name = "member3"
        data = {
            "email": member3_email,
            "username" : member3_name
        }
        feedback = PlayerModel.isValidPlayer(data)
        self.assertFalse(feedback["valid"])
        self.assertEqual(feedback["message"], 'invalid email')

        print("\n\n*************Test add invalid username Player***************\n\n")
        member4_email = "hguo@bsu.edu"
        member4_name = ""
        data = {
            "email": member4_email,
            "username" : member4_name
        }
        feedback = PlayerModel.isValidPlayer(data)
        print(feedback)
        self.assertFalse(feedback["valid"])
        self.assertEqual(feedback["message"],'username must be between 2 and 255  characters inclusive')

    def test2GameCreate(self):
        print("\n\n*************Test add new valid game with 7 teams**************\n\n")
        initiator = PlayerModel.findPlayerById(self.session, 1)
        #print ("Email: " + initiator.email)
        game = GameModel(initiator, "CS699", 60)
        team1 = TeamModel("Team 1")
        team2 = TeamModel("Team 2")
        team3 = TeamModel("Team 3")
        teams = [team1, team2, team3]
        initiator.team = team1
        self.session.flush()
        game.teams = teams
        self.session.add(game)
        self.session.commit()
        self.assertEqual(GameModel.numberOfRows(self.session),1)
        self.assertEqual(GameModel.getGameById(1,self.session),game)
        cGame = GameModel.getGameById(1,self.session)
        self.assertEqual(cGame.teams, teams)
        self.assertEqual(team1.gameId, 1)

        print("\n\n*************Test add invalid gamename **************************\n\n")
        gameData = {
            "maxPlayersPerTeam": 2,
            "turnDuration" : 30,
            "pointsToWin" : 30,
            "numberOfTeams": 2,
            "skipPenaltyAfter" : 3,
            "gameChangers" : True,
            "name":"",
            "initiatorTeam":{
            "name":"team1"
            },
            "teamData":[
            {"name":"team1"},
            {"name":"team2"}
            ]
        }
        feedback = GameModel.isValidGame(self.session,gameData)
        self.assertFalse(feedback["valid"])
        self.assertEqual(feedback["message"],'game name must be between 2 and 255 characters')

        print("\n\n*************Test add invalid turnDuration **************************\n\n")
        gameData = {
            "maxPlayersPerTeam": 2,
            "turnDuration" : 0,
            "pointsToWin" : 30,
            "numberOfTeams": 2,
            "skipPenaltyAfter" : 3,
            "gameChangers" : True,
            "name":"game123",
            "initiatorTeam":{
            "name":"team1"
            },
            "teamData":[
            {"name":"team1"},
            {"name":"team2"}
            ]
        }
        feedback = GameModel.isValidGame(self.session,gameData)
        self.assertFalse(feedback["valid"])
        self.assertEqual(feedback["message"],"turn duration must be between 30 and 120 inclusive")

        print("\n\n*************Test add invalid teams *****************************\n\n")
        gameData = {
            "maxPlayersPerTeam": 2,
            "turnDuration" : 30,
            "pointsToWin" : 30,
            "numberOfTeams": 0,
            "skipPenaltyAfter" : 3,
            "gameChangers" : True,
            "name":"game123",
            "initiatorTeam":{
            "name":"team1"
            },
            "teamData":[
            ]
        }
        feedback = GameModel.isValidGame(self.session,gameData)
        self.assertFalse(feedback["valid"])
        self.assertEqual(feedback["message"],"number of teams must be between 2 and 5 inclusive")

        print("\n\n*************Test add invalid players in one team *****************************\n\n")
        gameData = {
            "maxPlayersPerTeam": 10,
            "turnDuration" : 30,
            "pointsToWin" : 30,
            "numberOfTeams": 2,
            "skipPenaltyAfter" : 3,
            "gameChangers" : True,
            "name":"game123",
            "initiatorTeam":{
            "name":"team1"
            },
            "teamData":[
            {"name":"team1"},
            {"name":"team2"}
            ]
        }
        feedback = GameModel.isValidGame(self.session,gameData)
        self.assertFalse(feedback["valid"])
        self.assertEqual(feedback["message"],"number of players in a team must be between 2 and 5 inclusive")

        print("\n\n*************Test add invalid points to win *****************************\n\n")
        gameData = {
            "maxPlayersPerTeam": 2,
            "turnDuration" : 30,
            "pointsToWin" : 1,
            "numberOfTeams": 2,
            "skipPenaltyAfter" : 3,
            "gameChangers" : True,
            "name":"game123",
            "initiatorTeam":{
            "name":"team1"
            },
            "teamData":[
            {"name":"team1"},
            {"name":"team2"}
            ]
        }
        feedback = GameModel.isValidGame(self.session,gameData)
        self.assertFalse(feedback["valid"])
        self.assertEqual(feedback["message"],"points to win must be between 10 and 60 inclusive")

    def test3JoinTeam(self):
        player1 = PlayerModel.findPlayerById(self.session, 2)
        team1 = TeamModel.getTeamById(self.session, 1)
        cGame = GameModel.getGameById(1,self.session)
        player1.team = team1

        for i in range(1,8):
            team = TeamModel.getTeamById(self.session, i)
            player2 = PlayerModel.findPlayerById(self.session, 2*i)
            player3 = PlayerModel.findPlayerById(self.session, 2*i+1)
            player2.team = team
            player3.team = team
            i = i+1
            self.session.flush()
            self.session.commit()
        self.assertTrue(player1 in team1.players)
        self.assertTrue(player1.team == team1)

    def test4SaveCards(self):
        for index in range(50):
            forbidden = "['word1', 'word2', 'word3', 'word4']"
            card = CardModel("word_" + str(index + 1), forbidden, "Book", "345")
            self.session.add(card)
            self.session.flush()
        self.session.commit()
        self.assertEqual(CardModel.numberOfRows(self.session),50)


    def test5AddUsedCard(self):
        game = GameModel.getGameById(1,self.session)
        card = CardModel.findCardById(self.session, 2)
        game.addUsedCard(card)
        self.session.flush()
        self.session.commit()
        self.assertTrue(card in game.usedCards)
        unusedCards = game.getUnusedCards()
        self.assertEqual(len(unusedCards),49)


    def test6GameChanger(self):
        gameChangers = GameChangers()
        for i in range(100000):
            selectedGameChanger = gameChangers.rollDie()
            selectedGameChanger.count += 1
        for key, changer in gameChangers.changers.items():
            loss = abs(changer.count - (1000*changer.weight))/100000
            print(loss)
            self.assertLessEqual(loss,0.01)
            print("Weight: " + str(changer.weight) + ", Selected: " + str(changer.count))

    def test7CreateTurn(self):
        game = GameModel.getGameById(1,self.session)
        turn = game.createTurn()
        self.session.commit()
        obervers = turn.getObservers()
        guessers = turn.getGuessers()
        moderator = turn.getModerator()
        teller = turn.getTeller()
        teamOnDeck = turn.team
        print("On deck: " + teamOnDeck.name)
        print("Moderator: " + moderator.nickname)
        print("Teller: " + teller.nickname)
        self.session.close()

    def test8AddGameChanger(self):
        game = GameModel.getGameById(1,self.session)
        round = game.getCurrentRound()
        self.session.commit()
        turn = round.getCurrentTurn()
        turn.setGameChanger()
        print("Changer Number is {}".format(turn.gameChangerNumber))
        turn.updatePlayerRoles() # roles have to be updated if the all-guessers game changer is selected
        self.session.commit()
        self.session.close()

    def test9LoadCard(self):
        game = GameModel.getGameById(1,self.session)
        round = game.getCurrentRound()
        self.session.commit()
        turn = round.getCurrentTurn()
        cardData = turn.loadCard()
        print("buzzword: " + cardData['card']['buzzword'])
        self.session.commit()
        self.session.close()

if __name__ == "__main__":
    unittest.main()
