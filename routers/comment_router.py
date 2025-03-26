import logging
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from model.models import PostCommentRequest, Comment, EditCommentTextRequest, AllCommentsResponse, CommentWithReplies

router = APIRouter(prefix="/api/comments", tags=["comments"])

logger = logging.getLogger("__name__")


@router.post("/post")
async def post_comment(comment: PostCommentRequest, db: AsyncSession = Depends(get_db)):
    new_comment = Comment(
        author=comment.author,
        text=comment.text,
        image=comment.image,
    )

    logger.info(f"Adding new comment: {new_comment} to database")

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return {"message": "Comment posted!", "id": new_comment.id}


@router.put("/update/{comment_id}")
async def edit_comment(comment_id: int, edited_comment: EditCommentTextRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment)
        .where(Comment.id == comment_id)
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
    comment.image = edited_comment.image

    await db.commit()
    await db.refresh(comment)

    return {
        "message": "Comment updated successfully!",
        "id": comment.id,
        "text": comment.text,
        "image": comment.image
    }


@router.delete("/delete/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment)
        .where(Comment.id == comment_id)
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

    return {"message": "Comment deleted successfully!", "id": comment.id}


@router.get("/all", response_model=List[CommentWithReplies])
async def list_all_comments(db: AsyncSession = Depends(get_db)):
    # Fetch all the comments without parent
    result = await db.execute(
        select(Comment)
        .where(Comment.parent == None)
    )

    print(result)

    logger.info(f"Fetching comments from database with result {result} ", result)

    comments = result.scalars().all()

    logger.info(f"Fetching comments from database: ", comments)

    comments_with_replies = []

    # Iterate all root comments and append it to the result
    for comment in comments:
        comment_tree = await comment_tree_builder(comment.id, db)
        comments_with_replies.append(comment_tree)

    return comments_with_replies


# Build the tree structure for root comment
async def comment_tree_builder(comment_id: int, db: AsyncSession):
    # Check if the root comment exist
    parent_result = await db.execute(
        select(Comment)
        .where(Comment.id == comment_id)
    )

    parent_comment = parent_result.scalar_one_or_none()

    if not parent_comment:
        raise HTTPException(
            status_code=404,
            detail=f"Comment {comment_id} not found"
        )

    # Build the tree for the root comment
    comment_tree = CommentWithReplies.from_orm(parent_comment)

    # Fetch replies for the comment
    replies_result = await db.execute(
        select(Comment)
        .where(Comment.parent == comment_id)
    )
    replies = replies_result.scalars().all()

    # Iterate the replies and put it in root comment's replies
    for reply_result in replies:
        comment_with_replies = CommentWithReplies.from_orm(reply_result)
        comment = await comment_tree_builder(comment_with_replies.id, db)
        comment_tree.replies.append(comment)

    return comment_tree
