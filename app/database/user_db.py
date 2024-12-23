from sqlmodel import Session, select
from app.database.config import engine, create_tables
from app.models.user import UserData

def get_user(username: str) -> UserData:
    with Session(engine) as session:
        statement = select(UserData).where(UserData.username == username)
        result = session.exec(statement)
        user = result.one()
        return user

# to run if we need to create the "userdata" table - for the user
if __name__ == "__main__":
    create_tables()