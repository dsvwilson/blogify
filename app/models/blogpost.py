from sqlmodel import SQLModel, Field
from datetime import date

class BlogPostData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    date: date
    post_content: str
    slug: str