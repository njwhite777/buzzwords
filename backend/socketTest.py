import logging
#logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
#logging.basicConfig()
from socketIO_client import SocketIO,BaseNamespace,LoggingNamespace
import unittest
from app import Session,socketio,socketIOClients
from models.card import Card as CardModel
from models.game import Game as GameModel
from models.player import Player as PlayerModel
from models.round import Round as RoundModel
from models.team import Team as TeamModel
from models.turn import Turn as TurnModel




class GameNamespace(BaseNamespace):

    def on_connect(self):
        print('connect game namespace')

    def request_games(self):
        self.emit('request_games')

    def once_listen(self,data):
        print("I am listening!")
        print(data)
    def listen_game_list(self):
        self.on('game_list',self.once_listen)

class ViewNamespace(BaseNamespace):
    def on_connect(self):
        print('connect view namespace')

class TimerNamespace(BaseNamespace):
    def on_connect(self):
        print('connect timer namespace')

class PlayerNamespace(BaseNamespace):
    def on_connect(self):
        print('connect player namespace')

class CardNamespace(BaseNamespace):
    def on_connect(self):
        print('connect card namespace')
    def on_skip_card(self,data):
        print(data)

class TestSocket(unittest.TestCase):

    socketIO = SocketIO('localhost', 5000)
    game_namespace = socketIO.define(GameNamespace, '/io/game')
    view_namespace = socketIO.define(ViewNamespace, '/io/view')
    timer_namespace = socketIO.define(TimerNamespace, '/io/timer')
    player_namespace = socketIO.define(PlayerNamespace, '/io/player')
    joinTeam = None
    def __init__(self, *args, **kwargs):
        super(TestSocket, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        pass
    def setUp(self):
        pass

    ## Callback functions when socket listen actions
    def passLogInfo(self,data):
        self.loginfo = data

    def passInitGameData(self,data):
        self.initGame = data
    def passJoinTeamData(self,data):
        print("\n\nSome one join the team\n\n")
        self.joinTeam = data
        print(data)

    def passGameStartEnable(data1,data2):
        print("\n\nGame can start now!!!\n\n")

    def passGetCurrentGame(self, data):
        self.currentGame = data
        print("data is",data)
        print(self.currentGame)

    def passWheelInfo(self,data):
        self.currentWheel = data
        print("Roll wheel result is: {}".format(data))

    def passTurnRollResult(self,data):
        print("Turn roll result is: {}".format(data))
        self.turnRollResult = data
    def passTurnStart(self, data):
        print("start turn id is: {}".format(data))
        self.turnStart = data
    def passAllGuesser(self, data):
        print("pass all guesser changer is: {}".format(data))
        self.allGuesser = data
    ## End Callback functions
    def test1PlayerSocketLogin(self):
        info = {
            "email": "hguo1234@bsu.edu",
            "username": "qing1234"
        }
        self.player_namespace.on('player_logged_in',self.passLogInfo)
        self.player_namespace.emit("player_login",info)
        self.socketIO.wait(seconds=1)
        print("\n\n")
        print("****************************************************")
        print("*Test If user info passed Right********************")
        print("****************************************************")
        print("\n")
        self.assertEqual(self.loginfo["username"],info["username"])
        self.assertEqual(self.loginfo["email"],info["email"])
        self.assertTrue(self.loginfo["playerID"] is not None)


    def test2GameSocketInitGame(self):
        gameData = {
            "maxPlayersPerTeam": 2,
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
        self.game_namespace.on("created_game",self.passInitGameData)
        self.game_namespace.emit("init_game",gameData)
        self.socketIO.wait(seconds=1)
        print("\n\n")
        print("****************************************************")
        print("*Test Game Init info passed Right********************")
        print("****************************************************")
        print("\n")
        #Test Game name
        self.assertEqual(self.initGame["1"]["name"],gameData["name"])
        #Test team name
        self.assertEqual(self.initGame["1"]["teams"]["1"]["name"], gameData["teamData"][0]["name"])
        self.assertEqual(self.initGame["1"]["teams"]["2"]["name"], gameData["teamData"][1]["name"])
        #Test game config pass to team
        self.assertEqual(self.initGame["1"]["teams"]["1"]["maxPlayers"], gameData["maxPlayersPerTeam"])
        self.assertEqual(self.initGame["1"]["teams"]["2"]["maxPlayers"], gameData["maxPlayersPerTeam"])
        #Test initiator joined the first team
        self.assertEqual(self.initGame["1"]["teams"]["1"]["playerCount"],1)
        #Test game only has initiator joined at very begining
        self.assertEqual(self.initGame["1"]["teams"]["2"]["playerCount"],0)
        print("New Game Created here!:",self.initGame)

    def test3GameSocketJoinTeam(self):
        player1 = {
            "email": "player1@bsu.edu",
            "username": "Iam Player1"
        }
        # login new player and add it to DB
        self.player_namespace.on('player_logged_in',self.passLogInfo)
        self.player_namespace.emit("player_login",player1)

        # Let new player join game1 team1
        # Now the game has 3 players in it:
        # initiator team1
        # player1  team1
        player1JoinInfo = {'gameID':1,'teamID': 1,'player':player1["email"]}

        self.game_namespace.once('joined_team', self.passJoinTeamData)
        self.game_namespace.emit("join_team",player1JoinInfo)


        self.socketIO.wait(seconds=2)
        print("\n\n")
        print("****************************************************")
        print("*Test If player Joined Right Team********************")
        print("****************************************************")
        print("\n")
        # Test joined team player do right join!
        self.assertEqual(self.joinTeam['gameID'],player1JoinInfo["gameID"])
        self.assertEqual(self.joinTeam['id'],player1JoinInfo["gameID"])
        self.assertEqual(self.joinTeam['teams']['1']['name'],"team1")
        self.assertEqual(self.joinTeam['teams']['1']['id'],player1JoinInfo["teamID"])

    def test4GameValidateGameStart(self):

        # login new player as player2
        # let player2 join team2 game1
        player2 = {
            "email": "player2@bsu.edu",
            "username": "Iam Player2"
        }
        self.player_namespace.emit("player_login",player2)
        player2JoinInfo = {'gameID':1,'teamID': 2,'player':player2["email"]}
        self.game_namespace.emit("join_team",player2JoinInfo)
        # Now game1 has 3 players
        # initiator team1
        # player1   team1
        # player2   team2
        player3 = {
            "email": "player3@bsu.edu",
            "username": "Iam Player3"
        }
        self.view_namespace.on("show_game_start_button_enabled1",self.passGameStartEnable)
        self.game_namespace.on('joined_team', self.passJoinTeamData)
        self.player_namespace.emit("player_login",player3)
        player2JoinInfo = {'gameID':1,'teamID': 2,'player':player3["email"]}
        self.game_namespace.emit("join_team",player2JoinInfo)
        self.socketIO.wait(seconds=1)
        # Now game1 has 3 players
        # initiator team1
        # player1   team1
        # player2   team2
        # player3   team2

    def test5GameValidateStartGame(self):

        lastJoinedGame = {'gameID': 1}
        self.game_namespace.on("game_started", self.passGetCurrentGame)
        self.game_namespace.emit("start_game",lastJoinedGame)
        self.socketIO.wait(seconds=1)

        print("\n\n")
        print("****************************************************")
        print("*Test If start game button work********************")
        print("(1)*CurrentGame == startGame***********************")
        print("(2)*Create New Round*******************************")
        print("(3)*Create New Turn********************************")
        print("(4)*Assign Roles for Players************************")
        print("****************************************************")
        print("\n")
        # Test joined team player do right join!
        print("Test(1)*********************************************Pass")
        self.assertEqual(self.currentGame, lastJoinedGame)
        print("Test(2)*********************************************Pass")
        session = Session()
        turnID = 1
        roundID = 1
        round = RoundModel.getRoundById(roundID, session)
        turn = TurnModel.getTurnById(turnID,session)
        self.assertEqual(self.currentGame["gameID"], round.gameId)
        print("Test(3)*********************************************Pass")
        self.assertEqual(self.currentGame["gameID"], turn.gameId)
        self.assertEqual(round.id, turn.roundId)
        print("Test(4)********************************************Pass")

        teller_id = turn.turnTellerId
        moderator_id = turn.turnModeratorId
        player_teller = PlayerModel.findPlayerById(session, teller_id)
        player_moderator = PlayerModel.findPlayerById(session, moderator_id)
        # Test if teller from turn table has role of teller
        # Test if moderator from turn table has role of moderator
        self.assertEqual(player_teller.role,1)
        self.assertEqual(player_moderator.role,2)

    def test6GameRollWheel(self):

        wheel = {
            "gameID": 1,
            "duration": 4
        }
        self.game_namespace.on("my_roll_result", self.passWheelInfo)
        self.game_namespace.emit("roll_wheel",wheel)
        self.socketIO.wait(seconds=5)
        session = Session()
        turnID = 1
        turn = TurnModel.getTurnById(turnID,session)
        print("\n\n**********Test wheel result game changer write to DB*********Pass")
        self.assertEqual(self.currentWheel["rollID"],turn.gameChangerNumber)
        session.commit()
        session.close()



    def test7GameStartingTurn(self):

        currentGame = {'gameID': 1}

        print("************Test Start Turn***********************************Pass")
        self.game_namespace.on("roll_result", self.passTurnRollResult)
        self.game_namespace.on("turn_started", self.passTurnStart)
        self.game_namespace.emit("starting_turn",currentGame)
        self.socketIO.wait(seconds=1)
        print("***********Test Start New Turn in Same Game*******************Pass")
        session = Session()
        turnID = 1
        turn = TurnModel.getTurnById(turnID,session)
        self.assertEqual(self.turnRollResult["gameID"],1)
        print("***********Test roll result pass to turn table*******************Pass")
        self.assertEqual(self.turnRollResult["rollID"],turn.gameChangerNumber)
        session.commit()
        session.close()

    def test8GameChangerAllGuesser(self):
        wheel = {
            "gameID": 1,
            "duration": 4,
            "changerID": 7  #This is changer all guesser
        }
        self.game_namespace.on("my_roll_result_test", self.passAllGuesser)
        self.game_namespace.emit("roll_wheel_test",wheel)
        self.socketIO.wait(seconds=1)



if __name__ == "__main__":
    unittest.main()
