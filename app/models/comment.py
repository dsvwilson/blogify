from sqlmodel import SQLModel, Field
from datetime import date

class CommentData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: date
    content: str
    post_id: int = Field(foreign_key="blogpostdata.id")
    comment_genuinity: int