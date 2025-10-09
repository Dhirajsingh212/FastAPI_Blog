from fastapi import APIRouter, HTTPException, Path, Query
from dependency import user_dependency, db_dependency
from schemas import BlogRequest
from db.models import Blogs
from typing import Optional
from sqlalchemy import or_
from starlette import status

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", status_code=status.HTTP_200_OK)
async def create_new_blog(
    user: user_dependency, db: db_dependency, blog_request: BlogRequest
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    blog_model = Blogs(
        title=blog_request.title,
        description=blog_request.description,
        owner_id=user.get("id"),
    )

    db.add(blog_model)
    db.commit()


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_blog(
    user: user_dependency,
    db: db_dependency,
    page_number: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100),
    search: Optional[str] = Query(
        None, description="Search item for blog title or description"
    ),
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    query = db.query(Blogs).filter(Blogs.owner_id == user.get("id"))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(Blogs.title.ilike(search_term), Blogs.description.ilike(search_term))
        )

    total_count = query.count()

    blogs = query.offset(page_number * page_size).limit(page_size).all()

    return {
        "page_number": page_number,
        "page_size": page_size,
        "total_records": total_count,
        "data": blogs,
    }


@router.get("/{blog_id}", status_code=status.HTTP_200_OK)
async def get_blog_by_id(
    user: user_dependency, db: db_dependency, blog_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    blog_data = (
        db.query(Blogs)
        .filter(Blogs.owner_id == user.get("id"))
        .filter(Blogs.id == blog_id)
        .first()
    )
    if blog_data is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog_data


@router.put("/{blog_id}", status_code=status.HTTP_200_OK)
async def update_blog_by_id(
    user: user_dependency,
    db: db_dependency,
    blog_request: BlogRequest,
    blog_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    blog_data = (
        db.query(Blogs)
        .filter(Blogs.owner_id == user.get("id"))
        .filter(Blogs.id == blog_id)
        .first()
    )

    if blog_data is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_data.title = blog_request.title
    blog_data.description = blog_request.description

    db.add(blog_data)
    db.commit()


@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
async def delete_blog_by_id(
    user: user_dependency, db: db_dependency, blog_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    blog_data = (
        db.query(Blogs)
        .filter(Blogs.owner_id == user.get("id"))
        .filter(Blogs.id == blog_id)
        .first()
    )

    if blog_data is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.query(Blogs).filter(Blogs.owner_id == user.get("id")).filter(
        Blogs.id == blog_id
    ).delete()
    db.commit()
