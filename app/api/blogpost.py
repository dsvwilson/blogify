from fastapi import APIRouter, HTTPException
from app.services.classes.blogpost import BlogPost
from app.services.schema.blogpost import AddBlogPostSchema, EditBlogPostSchema
from app.models.blogpost import BlogPostData
from app.database.post_db import create_post_row, read_post, read_posts, update_post, delete_post_db

router = APIRouter()

# create a new blog post -> returns a "success" message alongside the post ID
@router.post("/posts/new", tags=["Posts"])
async def create_post(create: AddBlogPostSchema) -> str:
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
@router.get("/posts", tags=["Posts"])
async def all_posts(offset: int | None = 0, limit: int | None = 10) -> list[BlogPostData]:
    return read_posts(offset, limit)

# get a post - if unavailable, return an error message
@router.get("/posts/{post_id}", tags=["Posts"])
async def a_post(post_id: int) -> BlogPostData:
    post = read_post(post_id)
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} does not exist")
    
# update a post - if unavailable, return an error message
@router.patch("/posts/{post_id}", tags=["Posts"])
async def edit_post(post_id: int, edit: EditBlogPostSchema) -> str:
    post_edit = BlogPost()
    try:
        updated_post = post_edit.edit_post(post_id=post_id, edit=edit, read_post=read_post, data_model=BlogPostData)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} does not exist")
    update_post(id=post_id, title=updated_post.title, post_content=updated_post.post_content, slug=updated_post.slug)

    return f"Post {post_id} successfully edited"

# delete a post - if unavailable, return an error message
@router.delete("/posts/{post_id}", tags=["Posts"])
def delete_post(post_id: int):
    delete_operation = delete_post_db(post_id)
    if delete_operation:
        return delete_operation
    else:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} does not exist")