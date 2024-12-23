from sqlmodel import SQLModel, Field

class UserData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    full_name: str
    email: str
    hashed_password: str
    disabled: bool