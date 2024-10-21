from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST")

# engine = create_engine("sqlite:///krs.db")
# engine = create_engine("sqlite:///mydatabase.db")
# engine = create_engine("postgresql+psycopg2://postgres:password@0.0.0.0:5432/pomodoro")

engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}")
Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session()
