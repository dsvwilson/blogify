# external module imports
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends

# internal module imports
from app.services.classes.user import User
from app.models.blogpost import BlogPostData
from app.services.classes.blogpost import BlogPost
from app.services.schema.blogpost import AddBlogPostSchema, EditBlogPostSchema
from app.database.post_db import create_post_row, read_post, read_posts, update_post, delete_post_db

router = APIRouter()

# get the current user from the class methods for authentication purposes
async def get_current_active_user(current_user: Annotated[User, Depends(User.get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


# create a new blog post -> returns a "success" message alongside the post ID
#
# requires authentication
@router.post("/posts/new")
async def create_post(current_user: Annotated[User, Depends(get_current_active_user)], create: AddBlogPostSchema) -> str:
    blogpost = BlogPost(
        title=create.title, post_content=create.post_content
    )
    blogpost.date = blogpost.get_date()
    blogpost.slug = blogpost.build_slug()
    post_id = create_post_row(
        title=blogpost.title, date=blogpost.date, post_content=blogpost.post_content, slug=blogpost.slug
    )
    return f"Post {post_id} has been successfully created"

# get all the posts from the database with pagination defaulting to 10 elements -> returns a list of posts
@router.get("/posts")
async def all_posts(offset: int | None = 0, limit: int | None = 10) -> list[BlogPostData]:
    return read_posts(offset, limit)

# get a post - if unavailable, return an error message
@router.get("/posts/{post_id}")
async def a_post(post_id: int) -> BlogPostData:
    post = read_post(post_id)
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} does not exist")
    
# update a post - if unavailable, return an error message
#
# requires authentication
@router.patch("/posts/{post_id}")
async def edit_post(current_user: Annotated[User, Depends(get_current_active_user)], post_id: int, edit: EditBlogPostSchema) -> str:
    post_edit = BlogPost()
    try:
        updated_post = post_edit.edit_post(post_id=post_id, edit=edit, read_post=read_post, data_model=BlogPostData)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} does not exist")
    update_post(id=post_id, title=updated_post.title, post_content=updated_post.post_content, slug=updated_post.slug)

    return f"Post {post_id} successfully edited"

# delete a post - if unavailable, return an error message
#
# requires authentication
@router.delete("/posts/{post_id}")
def delete_post(current_user: Annotated[User, Depends(get_current_active_user)], post_id: int):
    delete_operation = delete_post_db(post_id)
    if delete_operation:
        return delete_operation
    else:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} does not exist")