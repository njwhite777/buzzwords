from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
Base = declarative_base()
from .card import Card as CardModel
from .game import Game as GameModel
from .player import Player as PlayerModel
from .round import Round as RoundModel
from .team import Team as TeamModel
from .turn import Turn as TurnModel
# from .gameround import GameRound as GameRoundModel
# from .gameteam import GameTeam as GameTeamModel
# from .round import Round as RoundModel
# from .user import User as UserModel


# testing inserting data:
card1 = CardModel()
#card1.buzzword = "Cohesion"
#card1.forbidden_words = "{'coupling', 'design', 'functional', 'strength'}"
#card1.skipped_count = 0
#card1.won_count = 0
#card1.lost_count = 0
#card1.source = "Book"
#card1.source_page = "436"
#session.add(card1)
