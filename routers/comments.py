from fastapi import APIRouter, Path, HTTPException
from dependency import user_dependency, db_dependency
from schemas import CommentRequest
from db.models import Comments, Blogs
from starlette import status

router = APIRouter(tags=["comments"])


@router.post("/{blog_id}/comment", status_code=status.HTTP_200_OK)
async def create_new_comment(
    user: user_dependency,
    db: db_dependency,
    comment_request: CommentRequest,
    blog_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    if db.query(Blogs).filter(Blogs.id == blog_id) is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    comment_model = Comments(
        description=comment_request.description,
        owner_id=user.get("id"),
        blog_id=blog_id,
    )

    db.add(comment_model)
    db.commit()


@router.get("/{blog_id}/comments/all", status_code=status.HTTP_200_OK)
async def get_all_comments_of_blog(
    user: user_dependency, db: db_dependency, blog_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authorized")

    comments = db.query(Comments).filter(Comments.blog_id == blog_id).all()

    return comments


@router.put("/{blog_id}/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment_by_id(
    user: user_dependency,
    db: db_dependency,
    comment_request: CommentRequest,
    blog_id: int = Path(gt=0),
    comment_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    if db.query(Blogs).filter(Blogs.id == blog_id).first() is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    comment_data = db.query(Comments).filter(Comments.id == comment_id).first()

    if comment_data is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment_data.owner_id != user.get("id"):
        raise HTTPException(
            status_code=400, detail="You are not authorized to perform this action"
        )

    comment_data.description = comment_request.description

    db.add(comment_data)
    db.commit()


@router.delete("/{blog_id}/comments/{comment_id}")
async def delete_comment_by_id(
    user: user_dependency,
    db: db_dependency,
    blog_id: int = Path(gt=0),
    comment_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    if db.query(Blogs).filter(Blogs.id == blog_id).first() is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    comment_data = db.query(Comments).filter(Comments.id == comment_id).first()

    if comment_data is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment_data.owner_id != user.get("id"):
        raise HTTPException(
            status_code=400, detail="You are not authorized to perform this action"
        )

    db.query(Blogs).filter(Blogs.id == blog_id).delete()
    db.commit()
