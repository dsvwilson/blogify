# external module import
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

# internal module imports
from app.services.classes.user import User
from app.models.comment import CommentData
from app.services.classes.comment import Comment
from app.services.schema.comment import CommentSchema
from app.database.post_db import read_post
from app.database.comment_db import new_comment, read_comments, read_comment, delete_comment_db

router = APIRouter()

# get the current user from the class methods for authentication purposes
async def get_current_active_user(current_user: Annotated[User, Depends(User.get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

# create a new comment
@router.post("/posts/{post_id}/comment/new")
async def post_comment(create: CommentSchema, post_id: int) -> str:
    # return an error if the post does not exist
    Comment.post_check(post_id, read_post, post_id, exception=HTTPException)

    comment = Comment(content=create.content)
    comment.date = comment.get_date()
    comment_id = new_comment(date=comment.date, content=comment.content, post_id=post_id)
    return f"Comment {comment_id} successfully added for post {post_id}"

# get all the comments associated with a certain post
@router.get("/posts/{post_id}/comments")
async def get_comments(post_id: int, offset: int | None = 0, limit: int | None = 10) -> list[CommentData]:
    # return an error if the post does not exist
    Comment.post_check(post_id, read_post, post_id, exception=HTTPException)

    return read_comments(post_id, offset, limit)

# get a comment by its ID - if unavailable, return a 404 error message
#
# requires authentication
@router.get("/posts/comment/{comment_id}")
async def get_a_comment(current_user: Annotated[User, Depends(get_current_active_user)], comment_id: int) -> CommentData:
    comment = read_comment(comment_id)
    if comment:
        return comment
    else:
        raise HTTPException(status_code=404, detail=f"Comment {comment_id} does not exist")

# delete a comment
#
# requires authentication
@router.delete("/posts/comment/{comment_id}")
def delete_comment(current_user: Annotated[User, Depends(get_current_active_user)], comment_id: int):
    delete_operation = delete_comment_db(comment_id)
    if delete_operation:
        return delete_operation
    else:
        raise HTTPException(status_code=404, detail=f"Comment {comment_id} does not exist")