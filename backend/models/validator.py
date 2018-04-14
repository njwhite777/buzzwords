import re

class Validator():

    @staticmethod
    def minLength(input, min):
        if min < 0:
            return False
        return input is not None and len(input) >= min

    @staticmethod
    def maxLength(input, max):
        if max < 0:
            return False
        return input is not None and len(input) <= max

    @staticmethod
    def isLengthBetween(input, min, max):
        return Validator.minLength(input, min) and Validator.maxLength(input, max)

    @staticmethod
    def isInt(input):
        try:
            intPart = int(input)
            return input - intPart == 0
        except:
            return False

    @staticmethod
    def isLessThanOrEqual(input, max):
        if max < 0:
            return False
        return Validator.isInt(input) and input <= max

    @staticmethod
    def isGreaterThanOrEqual(input, min):
        if min < 0:
            return False
        return Validator.isInt(input) and input >= min

    @staticmethod
    def isBetween(input, min, max):
        return Validator.isLessThanOrEqual(input, max) and Validator.isGreaterThanOrEqual(input, min)

    @staticmethod
    def isPrintable(input):
        return input is not None and input.isprintable()

    def isValidEmail(email):
        return re.match("[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def isValidPlayer(data):
        return Validator.isLengthBetween(data['username'], 2, 255) and Validator.isLengthBetween(data['email'], 2, 255) and Validator.isValidEmail(data['email'])

    def isValidGame(data):
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
