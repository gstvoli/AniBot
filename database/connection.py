from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///animebot.db')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)