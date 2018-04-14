import unittest
from app import engine, Session
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
        self.session.add(card)
        self.session.commit()

        card = CardModel.findCardById(self.session, 1)
        self.assertEqual(card.buzzword, "unit test")

    def testCountCard(self):
        self.assertEqual(CardModel.numberOfRows(self.session),1)

    def testRemoveForbiddenWords(self):
        card = CardModel.findCardById(self.session, 1)
        card.removeForbiddenWords()
        self.assertEqual(card.forbiddenWords,"")



if __name__ == "__main__":
    unittest.main()
