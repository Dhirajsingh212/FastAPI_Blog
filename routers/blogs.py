from fastapi import APIRouter, HTTPException
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
async def get_all_blog(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    blog_data = db.query(Blogs).filter(Blogs.owner_id == user.get("id")).all()
    return blog_data
