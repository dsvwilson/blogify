from pydantic import BaseModel


class CommentSchema(BaseModel):
    content: str