from dotenv import load_dotenv
import os
from sqlmodel import SQLModel, create_engine

# configuration information for the database, including the URL, accessing it, and creating a new database (by executing this entire file)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(url=DATABASE_URL)


# create the tables in the database
def create_tables():
    SQLModel.metadata.create_all(engine)