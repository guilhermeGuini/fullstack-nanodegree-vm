from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Connection:

    def connect(self):
        engine = create_engine("postgresql+psycopg2://postgres:alelo123@localhost:5432/postgres", connect_args={'options': '-csearch_path=test'})
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        return DBSession()