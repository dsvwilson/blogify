from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from classes import BlogPost
from schema import AddBlogPostSchema, EditBlogPostSchema
from db import BlogPostData, create_post_row, read_post, read_posts, update_post, delete_post_db

app = FastAPI()

@app.post("/posts/new")
async def create_post(create: AddBlogPostSchema) -> str:
    blogpost = BlogPost(
        title=create.title, post_content=create.post_content
    )
    blogpost.date = blogpost.get_date()
    blogpost.slug = blogpost.build_slug()
    post_id = create_post_row(
        title=blogpost.title, date=blogpost.date, post_content=blogpost.post_content, slug=blogpost.slug
    )
    return f"Successful!"


@app.get("/posts")
async def all_posts(offset: int | None = 0, limit: int | None = 10) -> list[BlogPostData]:
    return read_posts(offset, limit)


@app.get("/posts/{post_id}")
async def a_post(post_id: int) -> BlogPostData:
    post = read_post(post_id)
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="Post unavailable")
    

@app.patch("/posts/{post_id}")
async def edit_post(post_id: int, edit: EditBlogPostSchema) -> str:
    post_edit = BlogPost()
    try:
        updated_post = post_edit.edit_post(post_id=post_id, edit=edit, read_post=read_post, data_model=BlogPostData)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Post unavailable")
    update_post(id=post_id, title=updated_post.title, post_content=updated_post.post_content, slug=updated_post.slug)

    return "Successfully edited"

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    delete_operation = delete_post_db(post_id)
    if delete_operation:
        return delete_operation
    else:
        raise HTTPException(status_code=404, detail="Post unavailable")