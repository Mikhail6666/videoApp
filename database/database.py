from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqlite:///krs.db")
# engine = create_engine("sqlite:///mydatabase.db")
# engine = create_engine("postgresql+psycopg2://postgres:password@0.0.0.0:5432/pomodoro")
engine = create_engine("postgresql+psycopg2://postgres:Qq123456@0.0.0.0:5432/videoapp_db")
Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session()
