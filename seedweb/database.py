from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DevelopmentConfig

SQLALCHEMY_DATABASE_URL = DevelopmentConfig.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
