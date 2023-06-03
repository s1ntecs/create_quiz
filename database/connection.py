from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.quiz import Base

database_host = "database"
database_port = "5432"
database_name = "postgres"
database_user = "postgres"
database_password = "susel"

database_connection_string = (f"postgresql://{database_user}:"
                              f"{database_password}@{database_host}:"
                              f"{database_port}/{database_name}")
engine = create_engine(database_connection_string, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def conn():
    Base.metadata.create_all(bind=engine)
