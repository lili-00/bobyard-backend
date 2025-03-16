from fastapi import FastAPI
from routers.comment_router import router as comment_router

app = FastAPI()
app.include_router(comment_router)

