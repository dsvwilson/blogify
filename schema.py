from pydantic import BaseModel


class BlogPostSchema(BaseModel):
    title: str | None = None
    post_content: str | None = None

class AddBlogPostSchema(BlogPostSchema):
    title: str
    post_content: str

class EditBlogPostSchema(BlogPostSchema):
    pass