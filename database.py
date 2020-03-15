from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import datetime
Base = declarative_base()

class Record(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    application = Column(String)
    category = Column(String)
    data = Column(String)

class Logger(object):

    def __init__(self):
        database_string = os.environ['DATABASE']
        self.engine = create_engine(database_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def add(self, params):
        record = Record(**params)
        self.session.add(record)
        self.session.commit()

