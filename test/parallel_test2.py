import threading
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import threading


# capabilities = webdriver.DesiredCapabilities().FIREFOX
# capabilities["marionette"] = False
binary = FirefoxBinary(r'/usr/bin/firefox')

class CreateGame(threading.Thread):
    def __init__(self):
        super(CreateGame, self).__init__()
        self.hostname = "http://localhost"
        self.port = 9000
        self.gamename = "game3_3player_2team"
        self.teams = []
        self.usernames = []
        self.emails = []
        self.teamname1 = "hard"
        self.teamname2 = "easy"


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

        # set 3 players in each team
        playerNumber = driver.find_element_by_name("playerNumber")
        playerNumber.clear()
        playerNumber.send_keys(3)

        create = driver.find_element_by_name("create")
        time.sleep(2)
        create.click()


    def newBrowserWindow(self):
        return webdriver.Firefox(firefox_binary=binary)

    def openApplication(self,driver=None):
        if(not(driver)):
            self.driver.get(self.hostname+":"+str(self.port))
        else:
            driver.get(self.hostname+":"+str(self.port))



class JoinGame(threading.Thread):
    def __init__(self,useremail="hguo@bsu.edu", username="hanqing", gamename="game2",teamname="hard"):
        super(JoinGame,self).__init__()
        self.hostname = "http://localhost"
        self.port = 9000
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

        selectedGame = driver.find_element_by_xpath('//md-toolbar[@name="{}"]'.format(gamename))
        time.sleep(2)
        selectedGame.click()

        selectedTeam = driver.find_element_by_xpath('//button[@name="{}"]'.format(teamname))
        time.sleep(2)
        selectedTeam.click()

    def newBrowserWindow(self):
        return webdriver.Firefox(firefox_binary=binary)

    def openApplication(self,driver=None):
        if(not(driver)):
            self.driver.get(self.hostname+":"+str(self.port))
        else:
            driver.get(self.hostname+":"+str(self.port))

if __name__ == "__main__":
    # threadLock = threading.Lock()
    # threads = []
    #
    # threadLock.acquire()
    creator = CreateGame()
    creator.start()
    creator.join()
    #threadLock.release()


    client1 = JoinGame()
    client2 = JoinGame(username="hanqing2", useremail = "hguo2@bsu.edu", teamname = "easy")
    client3 = JoinGame(username="aron",useremail="aron@bsu.edu",teamname="hard")
    client4 = JoinGame(username="aron2",useremail="aron2@bsu.edu",teamname="easy")
    client5 = JoinGame(username="nate2",useremail = "nate2@bsu.edu",teamname = "easy")

    client1.start()
    client2.start()
    client3.start()
    client4.start()
    client5.start()
