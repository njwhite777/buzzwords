#!/usr/bin/env python

import threading
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n','--number',default=4,help='Number of players')
parser.add_argument('-u','--url',default="http://0.0.0.0",help='URL to use for the players to join.')
parser.add_argument('-c','--create',action='store_true',help='Have a player create the game.')
parser.add_argument('-g','--game',default='game1',help='Give a name to the game.')
parser.add_argument('-t','--teams',nargs='+',default="team1 team2",help='List the names of the teams that should be in the game.')
parser.add_argument('-p','--port',default=9000,help='The port to connect to for the client application.')

# capabilities = webdriver.DesiredCapabilities().FIREFOX
# capabilities["marionette"] = False
binary = FirefoxBinary(r'/usr/bin/firefox')

class CreateGame(threading.Thread):

    def __init__(self,useremail="hguo@bsu.edu", username="hanqing", gamename="game2",teamname="hard",url="0.0.0.0",port=9000,teams=list()):
        super(CreateGame, self).__init__()
        self.url = url
        self.port = port
        self.gamename = gamename
        self.teams = teams

    def run(self, driver =None):

        if(not driver):
            driver = self.newBrowserWindow()
        self.openApplication(driver)
        time.sleep(3)
        email = driver.find_element_by_name("email")
        email.send_keys("nate@bsu.edu")
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys("nate")
        submit = driver.find_element_by_name("submit")
        time.sleep(2)
        submit.click()
        gameName = driver.find_element_by_name("gamename")
        gameName.send_keys(self.gamename)

        teamName1 = driver.find_element_by_xpath('//input[@name="Team 1"]')
        teamName1.clear()
        teamName1.send_keys(self.teamname1)

        teamName2 = driver.find_element_by_xpath('//input[@name="Team 2"]')
        teamName2.clear()
        teamName2.send_keys(self.teamname2)

        playerNumber = driver.find_element_by_name("playerNumber")
        playerNumber.clear()
        playerNumber.send_keys(2)

        turnduration = driver.find_element_by_name("turn_duration")
        turnduration.click()
        duration = driver.find_element_by_xpath('//md-option[@value="60"]')
        duration.click()

        maxRoundsPerGame = driver.find_element_by_name("rounds_per_game")
        maxRoundsPerGame.clear()
        maxRoundsPerGame.send_keys(3)

        maxRoundsPerGame = driver.find_element_by_name("pointsToWin")
        maxRoundsPerGame.clear()
        maxRoundsPerGame.send_keys(10)

        freeskips = driver.find_element_by_name("free_skips")
        freeskips.click()
        skipNumber = driver.find_element_by_xpath('//md-option[@value="0"]')
        skipNumber.click()

        create = driver.find_element_by_name("create")
        time.sleep(2)
        create.click()

    def newBrowserWindow(self):
        return webdriver.Firefox(firefox_binary=binary)

    def openApplication(self,driver=None):
        if(not(driver)):
            self.driver.get(self.url+":"+str(self.port))
        else:
            driver.get(self.url+":"+str(self.port))

class JoinGame(threading.Thread):
    def __init__(self,useremail="hguo@bsu.edu", username="hanqing", gamename="game2",teamname="hard",url="0.0.0.0",port=9000):
        super(JoinGame,self).__init__()
        self.url = url
        self.port = port
        self.useremail = useremail
        self.username = username
        self.gamename = gamename
        self.teamname = teamname

    def run(self):
        self.joinTeam(self.useremail, self.username, self.gamename, self.teamname)


    def joinTeam(self,useremail, username, gamename, teamname, driver=None):
        if(not driver):
            driver = self.newBrowserWindow()
        self.openApplication(driver)
        time.sleep(3)
        email = driver.find_element_by_name("email")
        email.send_keys(useremail)
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys(username)
        submit = driver.find_element_by_name("submit")
        time.sleep(3)
        submit.click()

        selectedGame = driver.find_element_by_xpath('//md-toolbar[@name="{}"]'.format(self.gamename))
        selectedGame.click()
        time.sleep(3)

        selectedTeam = driver.find_element_by_xpath('//button[@name="{}.{}"]'.format(self.gamename,self.teamname))
        driver.execute_script("arguments[0].scrollIntoView();", selectedTeam)
        time.sleep(2)
        selectedTeam.click()

    def newBrowserWindow(self):
        return webdriver.Firefox(firefox_binary=binary)

    def openApplication(self,driver=None):
        if(not(driver)):
            self.driver.get(self.url+":"+str(self.port))
        else:
            driver.get(self.url+":"+str(self.port))
import sys

if __name__ == "__main__":
    # threadLock = threading.Lock()
    # threads = []
    #
    args = parser.parse_args()

    numPlayers = int(args.number)
    startIdx=1
    teams=args.teams.split()
    print(args)

    if(not(numPlayers % len(teams) == 0) and (not(args.create) and not(numPlayers % len(teams) == 1))):
        print("Sorry, teams must be balanced.")
        sys.exit(0)

    # if(args.create):
    #     creator = CreateGame(useremail="game_creator@bsu.edu", username="game_creator", gamename=args.game,url=args.url,port=args.port,teams=args.teams)
    #     startIdx = 1
    #
    players=list()

    for i in range(startIdx,numPlayers+startIdx):
        teamname = teams[i % len(teams)]
        players.append(JoinGame(username="player_{}".format(i),useremail="player_{}@bsu.edu".format(i),gamename=args.game,teamname="{}".format(teamname),url=args.url,port=args.port))

    for player in players:
        player.start()


    # # threadLock.acquire()
    # creator = CreateGame()
    # creator.start()
    # creator.join()
    # #threadLock.release()
    #
    #
    # client1 = JoinGame()
    # client2 = JoinGame(username="aron",useremail="aron@bsu.edu",teamname="easy")
    # client3 = JoinGame(username="aron2",useremail="aron2@bsu.edu",teamname="easy")
    #
    # client1.start()
    # client2.start()
    # client3.start()
