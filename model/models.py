from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Integer, Column, String, TIMESTAMP, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    author = Column(String(100), nullable=False)
    text = Column(Text)
    date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    likes = Column(Integer, default=0)
    image = Column(Text)


class PostCommentRequest(BaseModel):
    user_id: int
    author: str
    text: str


class EditCommentTextRequest(BaseModel):
    comment_id: int
    text: str


class AllCommentsResponse(BaseModel):
    comment_id: int
    user_id: int
    author: str
    text: str
    date: datetime
    likes: int
    image: str | None

    class Config:
        # orm_mode = True
        from_attributes = True
