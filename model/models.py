from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Integer, Column, String, TIMESTAMP, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(Text, nullable=False)
    text = Column(Text, nullable=True)
    date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    likes = Column(Integer, default=0)
    image = Column(Text, nullable=True)

    orm_mode = True




class PostCommentRequest(BaseModel):
    author: str
    text: str
    image: str


class EditCommentTextRequest(BaseModel):
    text: str
    image: str


class AllCommentsResponse(BaseModel):
    id: int
    author: str
    text: str
    date: datetime
    likes: int
    image: str | None

    class Config:
        # orm_mode = True
        from_attributes = True
