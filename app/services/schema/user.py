from pydantic import BaseModel

# user schema for when a registeration endpoint is created
class UserSchema(BaseModel):
    username: str
    full_name: str
    email_address: str
    disabled: bool = False
    password: str

class Login(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    username: str | None = None