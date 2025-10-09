from fastapi import APIRouter, HTTPException
from schemas import Token
from dependency import db_dependency, form_data_dependency
from auth.auth_util import authenticate_user, create_access_token
from starlette import status
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: form_data_dependency, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    else:
        token = create_access_token(user.username, user.id, timedelta(minutes=20))
        return {"access_token": token, "token_type": "bearer"}
