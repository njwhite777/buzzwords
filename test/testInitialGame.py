import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities["marionette"] = False
binary = FirefoxBinary(r'/usr/bin/firefox')


#setup different test cases as tuple

class testInitialGame(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(firefox_binary=binary, capabilities=capabilities)
        self.driver.get("localhost:9000")
        self.initGame1 = initGame(useremail="hguo@bsu.edu", username="")
        self.initGame2 = initGame(useremail="not email format", username="hello")
        self.initGame3 = initGame(useremail="hguo@bsu.edu", username="hanqing")
        self.initGame4 = initGame(useremail="hguo@bsu.edu", username="hanqing", gamename="helloGame1", numberofteam=3,
                                  teamname=["helloteam1", "helloteam2", "helloteam3"], numberofplayer="1")
        #
        #TODO: only 1 tema in this game, need to varify from backend to make "create" button unenable
        self.initGame5 = initGame(useremail="hguo@bsu.edu", username="hanqing", gamename="helloGame2", numberofteam=1,
                                  teamname=["helloteam1"], numberofplayer="1")

        #TODO: duplicate game name is invalid, need to varify from backend to make "create" button unenable
        self.initGame6 = initGame(useremail="hguo@bsu.edu", username="hanqing", gamename="helloGame1", numberofteam=3,
                                  teamname=["helloteam1", "helloteam2", "helloteam3"], numberofplayer="1")

        #TODO: length of gamename should larger than 2
        self.initGame7 = initGame(useremail="hguo@bsu.edu", username="hanqing", gamename="G", numberofteam=1,
                                  teamname=["helloteam1"], numberofplayer="1")
        self.initGame8 = initGame()
        self.initGame9 = initGame()

    def login(self, useremail, username):
        driver = self.driver
        email = driver.find_element_by_name("email")
        email.send_keys(useremail)
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys(username)
        submit = driver.find_element_by_name("submit")
        time.sleep(3)
        return submit

    def fillForm(self, gamename, numberofteam, teamname, numberofplayer):
        driver = self.driver
        gameName = driver.find_element_by_name("gamename")
        gameName.send_keys(gamename)
        numberOfTeams = driver.find_element_by_name("numberOfTeams")
        numberOfTeams.clear()
        numberOfTeams.send_keys(numberofteam)
        time.sleep(3)

        for i in range(1,numberofteam+1):
            teamName = "Team "+str(i)
            selectTeam = driver.find_element_by_xpath("//input[@name = '%s']" %teamName)
            selectTeam.send_keys(teamname[i-1])


    ########################################################
    # valid email, empty username => invalid
    ########################################################
    # def testCase1(self):
    #     submit = self.login(self.initGame1.useremail, self.initGame1.username)
    #     self.assertEqual(submit.is_enabled(),False)
    #
    # ########################################################
    # # invalid email, valid username => invalid
    # ########################################################
    # def testCase2(self):
    #     submit = self.login(self.initGame2.useremail, self.initGame2.username)
    #     self.assertEqual(submit.is_enabled(),False)
    #
    # ########################################################
    # # valid email, valid username => valid
    # ########################################################
    # def testCase3(self):
    #     submit = self.login(self.initGame3.useremail, self.initGame3.username)
    #     self.assertEqual(submit.is_enabled(),True)

    ########################################################
    # valid email, empty username => invalid
    ########################################################
    def testCase4(self):
        submit = self.login(self.initGame4.useremail, self.initGame4.username)
        submit.click()
        self.fillForm(self.initGame4.gamename, self.initGame4.numberofteam, self.initGame4.teamname, self.initGame4.numberofplayer)

    def testCase5(self):
        pass
    # def testCase6(self):
    #     pass
    # def testCase7(self):
    #     pass
    # def testCase8(self):
    #     pass
    # def testCase9(self):
    #     pass


class initGame():

    def __init__(self, useremail=None, username=None, gamename=None, numberofteam=None, teamname=None,
                 numberofplayer=None, joingamename=None, joingameteam=None, creategame = True):
        self.useremail = useremail
        self.username = username
        self.gamename = gamename
        self.numberofteam = numberofteam
        self.teamname = teamname
        self.numberofteam = numberofteam
        self.numberofplayer = numberofplayer
        self.joingamename = joingamename
        self.joingameteam = joingameteam
        self.creategame = creategame

if __name__ == "__main__":
    unittest.main()
