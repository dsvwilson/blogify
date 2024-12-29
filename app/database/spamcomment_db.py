from sqlmodel import Session
from app.database.config import engine, create_tables
from app.models.spamcomment import SpamCommentData
from app.models.blogpost import BlogPostData
from datetime import date


# save a comment to spam and return its ID
def save_comment_to_spam(date: date, content: str, post_id: int, comment_genuinity: int) -> int:
    spamcomment = SpamCommentData(date=date, content=content, post_id=post_id, comment_genuinity=comment_genuinity)

    with Session(engine) as session:
        session.add(spamcomment)
        session.commit()
        session.refresh(spamcomment)

    return spamcomment.id


# to run if we need to create the "spamcommentdata" table - for spem comments
if __name__ == "__main__":
    create_tables()
