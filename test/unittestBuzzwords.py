import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities["marionette"] = False
binary = FirefoxBinary(r'/usr/bin/firefox')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class unittestBuzzword(unittest.TestCase):

    hostname = "localhost"
    port = 9000

    def setUp(self):
        self.driver = webdriver.Firefox(firefox_binary=binary, capabilities=capabilities)
        #self.driver.get("localhost:9000")


    def newBrowserWindow(self):
        return webdriver.Firefox(firefox_binary=binary, capabilities=capabilities)

    def openApplication(self,driver=None):
        if(not(driver)):
            self.driver.get(self.hostname+":"+str(self.port))
        else:
            driver.get(self.hostname+":"+str(self.port))

    # def testGamename(self):
    #     driver = self.driver
    #     #self.assertEqual("Buzzwords",driver.title)
    #     gameName = driver.find_element_by_name("gamename")
    #     gameName.send_keys("hanqing game")
    #
    # def testNumberOfTeams(self):
    #     numberOfTeams = self.driver.find_element_by_name("numberOfTeams")
    #     numberOfTeams.send_keys(10)

    def testMultiClientStart(self,n=4):
        drivers = [ self.newBrowserWindow() for i in range(0,n) ]

        for driver in drivers:
            self.openApplication(driver)

    def testJoinGame(self,driver=None):
        if (not (driver)):
            driver = self.driver
        email = driver.find_element_by_name("email")
        email.send_keys("nate@bsu.edu")
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys("nate")
        submit = driver.find_element_by_name("submit")
        time.sleep(3)
        submit.click()

    def testclient2testJoinGame(self,driver=None):
        if (not(driver)):
            driver = self.driver
        email = driver.find_element_by_name("email")
        email.send_keys("hguo@bsu.edu")
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys("hanqing")



    # def testCreateGame(self):
    #     teamNumberTest = 2
    #     driver = self.driver
    #     email = driver.find_element_by_name("email")
    #     email.send_keys("hguo@bsu.edu")
    #     playername = driver.find_element_by_name("playername")
    #     playername.clear()
    #     playername.send_keys("hanqing")
    #     submit = driver.find_element_by_name("submit")
    #     time.sleep(5)
    #     submit.click()
    #
    #     gameName = driver.find_element_by_name("gamename")
    #     gameName.send_keys("hanqing game1")
    #     numberOfTeams = driver.find_element_by_name("numberOfTeams")
    #     numberOfTeams.clear()
    #     numberOfTeams.send_keys(teamNumberTest)
    #     # teamName = []
    #     #
    #     # for i in range(0,teamNumberTest):
    #     #     teamName[i] = driver.find_element_by_name("team1")
    #     #     teamName[i].clear()
    #     #     if(i==0):
    #     #         teamName[i].send_keys("NateTeam")
    #     #     else:
    #     #         teamName[i].send_keys("AronTeam")
    #     # #TODO: apply to find teamname
    #     whichTeam = driver.find_element_by_name("whichTeam")
    #     time.sleep(5)
    #     whichTeam.click()
    #
    #     teamChoice = driver.find_element_by_name("joinTeam")
    #     teamChoice = WebDriverWait(driver, 3).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "md-option[value = 'team1']")))
    #     teamChoice.click()
    #
    #     playerNumber = driver.find_element_by_name("playerNumber")
    #     playerNumber.clear()
    #     playerNumber.send_keys(2)
    #
    #
    #
    #     create = driver.find_element_by_name("create")
    #
    #     time.sleep(3)
    #
    #     create.click()
    #
    #     time.sleep(2)




if __name__ == "__main__":
    unittest.main()

