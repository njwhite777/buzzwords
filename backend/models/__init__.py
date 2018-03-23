from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
Base = declarative_base()
from .card import Card as CardModel
# from .game import Game as GameModel
# from .gameround import GameRound as GameRoundModel
# from .gameteam import GameTeam as GameTeamModel
# from .round import Round as RoundModel
# from .team import Team as TeamModel
# from .user import User as UserModel
