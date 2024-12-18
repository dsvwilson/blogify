from sqlmodel import Session, select
from .config import engine
from app.models.blogpost import BlogPostData
from datetime import date

def create_post_row(title: str, date: date, post_content: str, slug: str) -> int:
    blogpost = BlogPostData(title=title, date=date, post_content=post_content, slug=slug)

    with Session(engine) as session:
        session.add(blogpost)
        session.commit()
        session.refresh(blogpost)

    return blogpost.id

def read_posts(offset: int = None, limit: int = None) -> list[BlogPostData]:
    with Session(engine) as session:
        statement = select(BlogPostData).offset(offset).limit(limit)
        result = session.exec(statement)
        return result.all()
    
def read_post(id: int) -> BlogPostData:
    with Session(engine) as session:
        return session.get(BlogPostData, id)
    
def update_post(id: int, title: str | None = None, post_content: str | None = None, slug: str | None = None) -> bool:
    with Session(engine) as session:
        blogpost = session.get(BlogPostData, id)

        if title:
            blogpost.title = title
        if post_content:
            blogpost.post_content = post_content
        if slug:
            blogpost.slug = slug

        session.add(blogpost)
        session.commit()
        session.refresh(blogpost)

def delete_post_db(id: int) -> str:
    with Session(engine) as session:
        blogpost = session.get(BlogPostData, id)
        if not blogpost:
            return None
        session.delete(blogpost)
        session.commit()
    return f"Post {id} has been permanently deleted."