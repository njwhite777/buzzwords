#!/usr/bin/env python

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time


# capabilities = webdriver.DesiredCapabilities().FIREFOX
# capabilities["marionette"] = False
binary = FirefoxBinary(r'/usr/bin/firefox')

class multiClient():
    def __init__(self):
        self.hostname = "http://localhost"
        self.port = 9000
        self.gamename = "game2"
        self.teams = []
        self.usernames = []
        self.emails = []
        self.teamname1 = "hard"
        self.teamname2 = "easy"

    def newBrowserWindow(self):
        return webdriver.Firefox(firefox_binary=binary)

    def openApplication(self,driver=None):
        if(not(driver)):
            self.driver.get(self.hostname+":"+str(self.port))
        else:
            driver.get(self.hostname+":"+str(self.port))


    def testMultiClientStart(self,n=4):
        drivers = [ self.newBrowserWindow() for i in range(0,n) ]

        for driver in drivers:
            self.openApplication(driver)

    def client1(self,driver=None):

        if(not driver):
            driver = self.newBrowserWindow()
        self.openApplication(driver)
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

        create = driver.find_element_by_name("create")
        time.sleep(2)
        create.click()

    def client2(self,driver=None):
        if (not driver):
            driver = self.newBrowserWindow()
        self.openApplication(driver)
        email = driver.find_element_by_name("email")
        email.send_keys("hguo@bsu.edu")
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys("hanqing")
        submit = driver.find_element_by_name("submit")
        time.sleep(2)
        submit.click()

        selectedGame = driver.find_element_by_xpath('//md-toolbar[@name="{}"]'.format(self.gamename))
        time.sleep(2)
        selectedGame.click()

        selectedTeam = driver.find_element_by_xpath('//button[@name="hard"]')
        time.sleep(2)
        selectedTeam.click()



    def client3(self,driver=None):
        if (not driver):
            driver = self.newBrowserWindow()
        self.openApplication(driver)
        email = driver.find_element_by_name("email")
        email.send_keys("aron@bsu.edu")
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys("aron")
        submit = driver.find_element_by_name("submit")
        time.sleep(2)
        submit.click()

        selectedGame = driver.find_element_by_xpath('//md-toolbar[@name="{}"]'.format(self.gamename))
        time.sleep(2)
        selectedGame.click()

        selectedTeam = driver.find_element_by_xpath('//button[@name="easy"]')
        time.sleep(2)
        selectedTeam.click()


    def client4(self,driver = None):
        if (not driver):
            driver = self.newBrowserWindow()
        self.openApplication(driver)
        email = driver.find_element_by_name("email")
        email.send_keys("aron2@bsu.edu")
        playername = driver.find_element_by_name("playername")
        playername.clear()
        playername.send_keys("aron2")
        submit = driver.find_element_by_name("submit")
        time.sleep(2)
        submit.click()

        selectedGame = driver.find_element_by_xpath('//md-toolbar[@name="{}"]'.format(self.gamename))
        time.sleep(2)
        selectedGame.click()

        selectedTeam = driver.find_element_by_xpath('//button[@name="easy"]')
        time.sleep(2)
        selectedTeam.click()


if __name__ == "__main__":

    mul = multiClient()
    mul.client1()
    mul.client2()
    mul.client3()
    mul.client4()
