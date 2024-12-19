from fastapi import FastAPI
from app.api import blogpost, comment

api_groups = [
    {
        "name": "Posts"
    },
    {
        "name": "Comments"
    }
]

app = FastAPI(openapi_tags=api_groups)

app.include_router(blogpost.router, tags=["Posts"], prefix="/v1")
app.include_router(comment.router, tags=["Comments"], prefix="/v1")