from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL  = "sqlite:///./kui.db"

engine  = create_engine(url=DB_URL ,connect_args={"check_same_thread": False} , echo=True)

SessionLocal =  sessionmaker(autocommit=False , autoflush=False , bind=engine)


Base =  declarative_base()


def get_db():
    session  =  SessionLocal()
    try:
        yield session
    
    except:
        session.close()