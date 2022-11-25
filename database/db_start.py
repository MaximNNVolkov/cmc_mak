from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


DATABASE = {
    'drivername': 'sqlite',
    'database': 'test.db'
}
engine = create_engine(URL(**DATABASE))
DeclarativeBase = declarative_base()


class Users(DeclarativeBase):
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    user_name = Column('user_name', String)
    admin = relationship('Admin', backref='user', uselist=False)

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_name': self.user_name,
            'admin': self.admin
        }


class UserSales(DeclarativeBase):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    date = Column('date', String)
    bch = Column('bch', Integer)
    sup = Column('sup', Integer)
    szdor = Column('szdor', Integer)


class Admin(DeclarativeBase):
    __tablename__ = 'admin'

    user_id = Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True)
    referer = Column('ref_id', Integer)
    created_on = Column(DateTime(), default=datetime.now)


def db_conn():
    engine = create_engine(URL(**DATABASE))
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
