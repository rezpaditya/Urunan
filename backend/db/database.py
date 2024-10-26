from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./data/urunan/urunan.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def initialize_table(target, connection, **kw):
    connection.execute(target.insert(), [
    {'email': 'user1'},
    {'email': 'user2'},
    {'email': 'user3'},
    {'email': 'user4'}
    ])
