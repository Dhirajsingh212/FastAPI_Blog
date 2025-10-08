from fastapi import APIRouter, HTTPException
from dependency import db_dependency, user_dependency
from schemas import UserRequest, UserResponse, PasswordRequest
from db.models import Users
from auth.auth_util import password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_new_user(db: db_dependency, user_request: UserRequest):
    if (
        db.query(Users).filter(Users.username == user_request.username).first()
        is not None
    ):
        raise HTTPException(status_code=400, detail="Username already exists")

    user_model = Users(
        username=user_request.username,
        firstname=user_request.firstname,
        lastname=user_request.lastname,
        password=password_hash.hash(user_request.password),
    )

    db.add(user_model)
    db.commit()


@router.get("/")
async def get_user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
    )


@router.put("/forgot_password")
async def change_password(
    user: user_dependency, db: db_dependency, request: PasswordRequest
):
    if user is None:
        raise HTTPException(status_code=400, detail="User not authenticated")

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not password_hash.verify(request.password, user_data.password):
        raise HTTPException(status_code=401, detail="Password incorrect")

    user_data.password = password_hash.hash(request.new_password)
    db.add(user_data)
    db.commit()


@router.get("/all")
async def get_all_users(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="User not authorized")
    return db.query(Users).all()
