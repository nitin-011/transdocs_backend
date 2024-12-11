from db import Base, engine, get_db
from models.user import User

# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)