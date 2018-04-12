import unittest
import sys
sys.path.append("..")
import os
print(os.getcwd())
from backend.app import engine, Session
from models import Base as AppModelBase
from db import delete_db
from models import CardModel, PlayerModel, TeamModel, GameModel, GameChanger, GameChangers, RoundModel
import random
from constants import *


class TestCard(unittest.TestCase):

    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def testSaveCard(self):
        delete_db(engine)
        AppModelBase.metadata.create_all(engine)
        forbidden = "{'word1', 'word2', 'word3', 'word4'}"
        card = CardModel(buzzword = "unit test", forbidden_words = forbidden, source = "Book",
         source_page = "345",skipped_count = 0, won_count = 0, lost_count = 0, is_phrase = IS_PHRASE)
        session.add(card)
        session.commit()

        card = CardModel.findCardById(session, 1)
        assertEqual(card.buzzword, "unit test")

    def testJoinGame(self,driver=None):
        pass


if __name__ == "__main__":
    unittest.main()
