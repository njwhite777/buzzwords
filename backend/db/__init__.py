from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_operations import create_db,delete_db,exists_db
Base = declarative_base()

def create_app_database(uri,rebuilddb=False):
    engine = create_engine(uri)
    # engine = create_engine(uri, echo=True)
    Session=sessionmaker(bind=engine)
    if(rebuilddb):
        if(exists_db(engine)):
            delete_db(engine)

        from models import CardModel
        from models import PlayerModel
        from models import TeamModel
        from models import GameModel
        from models import RoundModel
        from models import TurnModel

        create_db(engine)
        Base.metadata.create_all(engine)
    return Session,engine
