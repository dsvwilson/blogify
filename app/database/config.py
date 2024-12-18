from dotenv import load_dotenv
import os
from sqlmodel import SQLModel, create_engine

# configuration information for the database, including the URL, accessing it, and creating a new database (by executing this entire file)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(url=DATABASE_URL)


# residual code to create a database
def create_database():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_database()