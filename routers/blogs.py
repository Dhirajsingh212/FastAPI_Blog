from fastapi import APIRouter, HTTPException, Path, Query
from dependency import user_dependency, db_dependency
from schemas import BlogRequest
from db.models import Blogs

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/")
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


@router.get("/all")
async def get_all_blog(
    user: user_dependency,
    db: db_dependency,
    page_number: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100),
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    blog_data = (
        db.query(Blogs)
        .filter(Blogs.owner_id == user.get("id"))
        .offset(page_number * page_size)
        .limit(page_size)
        .all()
    )

    total_count = db.query(Blogs).filter(Blogs.owner_id == user.get("id")).count()

    return {
        "page_number": page_number,
        "page_size": page_size,
        "total_records": total_count,
        "data": blog_data,
    }


@router.get("/{blog_id}")
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


@router.put("/{blog_id}")
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


@router.delete("/{blog_id}")
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
