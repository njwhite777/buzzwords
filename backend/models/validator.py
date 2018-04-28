import re

class Validator():
    """ validation of user input """

    @staticmethod
    def minLength(input, min):
        """
            - checks if the input has at least min characters
            :param input: the parameter whose length has to be validated
            :type input: string
            :return: True if input has at least min characters, False otherwise
            :rtype: bool
        """
        input = input.strip()
        if min < 0:
            return False
        return input is not None and len(input) >= min

    @staticmethod
    def maxLength(input, max):
        """
            - checks if the input has at most max characters
            :param input: the parameter whose length has to be validated
            :type input: string
            :return: True if input has at most max characters, False otherwise
            :rtype: bool
        """
        input = input.strip()
        if max < 0:
            return False
        return input is not None and len(input) <= max

    @staticmethod
    def isLengthBetween(input, min, max):
        """
            - checks if the input has between min and max characters inclusive
            :param input: the parameter whose length has to be validated
            :type input: string
            :param min: the minimum number of characters input can have
            :type min: int
            :param max: the maximum number of characters input can have
            :type max: int
            :return: True if input has between min and max charcters inclusive
            :rtype: bool
        """
        return Validator.minLength(input, min) and Validator.maxLength(input, max)

    @staticmethod
    def isInt(input):
        """
            - checks if the input can be converted to an integer
            :param input: the parameter which has to be validated
            :type input: string
            :return: True if input can be converted to an integer, False otherwise
            :rtype: bool
        """
        try:
            intPart = int(input)
            return input - intPart == 0
        except:
            return False

    @staticmethod
    def isLessThanOrEqual(input, max):
        """
            - checks if the integer value of the input is at most max
            :param input: the parameter which is to be validated
            :type input: integer, string convertible to integer
            :param max: the maximum value input can be
            :type max: int
            :return: True if input is less than or equal to max, False otherise
            :rtype: bool
        """
        if max < 0:
            return False
        return Validator.isInt(input) and input <= max

    @staticmethod
    def isGreaterThanOrEqual(input, min):
        """
            - checks if the integer value of the input is at least min
            :param input: the parameter which is to be validated
            :type input: integer, string convertible to integer
            :param min: the minimum value input can be
            :type min: int
            :return: True if input is greater than or equal to min, False otherise
            :rtype: bool
        """
        if min < 0:
            return False
        return Validator.isInt(input) and input >= min

    @staticmethod
    def isBetween(input, min, max):
        """
            - checks if the value of input lies between min and max inclusive
            :param input: the parameter which is to be validated
            :type input: integer, string convertible to integer
            :param min: the minimum value input can be
            :type min: int
            :param max: the maximum value input can be
            :type max: int
            :return: True if the value of input lies between min and max
            :rtype: bool
        """
        return Validator.isLessThanOrEqual(input, max) and Validator.isGreaterThanOrEqual(input, min)

    @staticmethod
    def isPrintable(input):
        """
            - checks if all the characters in input are printable
            :param input: the parameter to be validated
            :type param: string
            :return : True if all characters in input are printable, False otherwise
            :rtype: bool
        """
        return input is not None and input.isprintable()

    def isValidEmail(email):
        """
            - checks if the email is valid
            :param email: the email to be validated
            :type email: string
            :return: True is the email is valid, False otherwise
            :rtype: bool
        """
        email = email.strip()
        return re.match("[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def isValidPlayer(data):
        """
            - validates all the player input received from the client application
            :param data: user input in a dictionary
            :type data: dictionary
            :return: dictionary with key "valid" equal to True if the all inputs are valid, otherwise:  "valid" = False, key "message" containing the error message
            :rtype: dictionary
        """
        if not Validator.isLengthBetween(data['username'], 2, 255):
            return {'valid' : False, 'message' : 'username must be between 2 and 255  characters inclusive'}
        elif not Validator.isValidEmail(data['email']):
            return {'valid' : False, 'message' : 'invalid email'}
        return {'valid' : True, 'message' : 'valid'}

    def isValidGame(data):
        """
            - validates all the game input received from the client application
            :param data: user input in a dictionary
            :type data: dictionary
            :return: dictionary with key "valid" equal to True if the all inputs are valid, otherwise:  "valid" = False, key "message" containing the error message
            :rtype: dictionary
        """
        # game length
        minGameLength = 2
        maxGameLength = 255
        # turn duration
        minTurnDuration = 30
        maxTurnDuration = 120
        # number of teams
        minNumberOfTeams = 2
        maxNumberOfTeams = 5
        # number of players per team
        minNumberOfPlayersPerTeam = 2
        maxNumberOfPlayersPerTeam = 5
        # points to win
        minNumberOfPointsToWin = 10
        maxNumberOfPointsToWin = 60

        if (not Validator.isLengthBetween(data['name'], minGameLength, maxGameLength)):
            return {'valid' : False, 'message' : 'game name must be between ' + str(minGameLength) + ' and ' + str(maxGameLength) + ' characters'}
        elif (not Validator.isBetween(data['turnDuration'],minTurnDuration,maxTurnDuration)):
            return {'valid' : False, 'message' : 'turn duration must be between ' + str(minTurnDuration) + ' and ' + str(maxTurnDuration) + ' inclusive'}
        elif (not Validator.isBetween(data['numberOfTeams'],minNumberOfTeams,maxNumberOfTeams)):
            return {'valid' : False, 'message' : 'number of teams must be between ' + str(minNumberOfTeams) + ' and ' + str(maxNumberOfTeams) + ' inclusive'}
        elif (not Validator.isBetween(data['maxPlayersPerTeam'],minNumberOfPlayersPerTeam,maxNumberOfPlayersPerTeam)):
            return {'valid' : False, 'message' : 'number of players in a team must be between ' + str(minNumberOfPlayersPerTeam) + ' and ' + str(maxNumberOfPlayersPerTeam) + ' inclusive'}
        elif (not Validator.isBetween(data['pointsToWin'],minNumberOfPointsToWin,maxNumberOfPointsToWin)):
            return {'valid' : False, 'message' : 'points to win must be between ' + str(minNumberOfPointsToWin) + ' and ' + str(maxNumberOfPointsToWin) + ' inclusive'}
        else:
            return {'valid' : True, 'message' : 'Valid'}
