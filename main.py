from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.comment_router import router as comment_router

app = FastAPI()
app.include_router(comment_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # List of allowed methods
    allow_headers=["*"],  # List of allowed headers
)
