from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from model.models import PostCommentRequest, Comment, EditCommentTextRequest, AllCommentsResponse

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.post("/post")
async def post_comment(comment: PostCommentRequest, db: AsyncSession = Depends(get_db)):
    new_comment = Comment(
        user_id=comment.user_id,
        text=comment.text,
        author=comment.author
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return {"message": "Comment posted!", "comment_id": new_comment.comment_id}


@router.put("/update/{comment_id}")
async def edit_comment(comment_id: int, edited_comment: EditCommentTextRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment)
        .where(Comment.comment_id == comment_id)
    )

    comment = result.scalar_one_or_none()

    # Raise exception if comment not found
    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Cannot find the comment. "
        )

    # Update the comment
    comment.text = edited_comment.text

    await db.commit()
    await db.refresh(comment)

    return {"message": "Comment updated successfully!", "comment_id": comment.comment_id, "updated_text": comment.text}


@router.delete("/delete/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment)
        .where(Comment.comment_id == comment_id)
    )

    comment = result.scalar_one_or_none()

    # Raise exception if comment not found
    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Cannot find the comment to delete. "
        )

    await db.delete(comment)
    await db.commit()

    return {"message": "Comment deleted successfully!", "comment_id": comment.comment_id}


@router.get("/all", response_model=List[AllCommentsResponse])
async def list_all_comments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment)
    )

    comments = result.scalars().all()

    return comments
