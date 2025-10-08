from database import Base, engine
from models import *  # импорт всех моделей

def create_all_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_all_tables()
