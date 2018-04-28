from app import engine, Session
from models import Base as AppModelBase
from db import delete_db
from models import CardModel, PlayerModel, TeamModel, GameModel, GameChanger, GameChangers, RoundModel
import random
import unittest
from constants import *

session = Session()
game = GameModel.getGameById(1, session)

# turn = game.createTurn()
# session.commit()

print(game.hasAtLeastOneRound())
print(game.teamsHaveEqualTurns())
print(game.teamHasReachedThreshold())
print(game.isGameOver())
session.close()
