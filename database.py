from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import datetime
Base = declarative_base()

import sys

class Record(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    application = Column(String)
    category = Column(String)
    key = Column(String)
    value = Column(String)

class Pair(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    application = Column(String)
    token = Column(String)
    ori_seg = Column(String)
    des_seg = Column(String)

class Logger(object):

    def __init__(self, application, ignore=False):
        self.application = application
        self.ignore = ignore
        try:
            database_string = os.environ['DATABASE']
            self.engine = create_engine(database_string)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            Base.metadata.create_all(self.engine)
        except:
            if not self.ignore:
                raise Exception()


    def add(self, params):
        try:
            params['application'] = self.application
            record = Record(**params)
            self.session.add(record)
            self.session.commit()
        if not self.ignore:
            raise Exception()

    def add_pair(self, params):
        try:
            params['application'] = self.application
            pair = Pair(**params)
            self.session.add(pair)
            self.session.commit()
        if not self.ignore:
            raise Exception()

