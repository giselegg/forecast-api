
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from crud.users import (
    retrieve_all_users,
    retrieve_user_by_id,
    retrieve_user_by_username,
    update_user,
    remove_user
)
from database.config import SessionLocal
from database.get_db import get_db
from schemas.users import UpdateUserSchema
from services.auth import check_authorization, check_user_id


# Security
security = HTTPBasic()

# Routes
users_router = APIRouter(prefix="/users")


@users_router.get("", status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials):
        if result := retrieve_all_users(db):
            return result


@users_router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials) and check_user_id(user_id, db, credentials):
        if result := retrieve_user_by_id(db, user_id):
            return result


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials) and check_user_id(user_id, db, credentials):
        if remove_user(db, user_id):
            return Response(status_code=status.HTTP_204_NO_CONTENT)


@users_router.put("/{user_id}", status_code=status.HTTP_201_CREATED)
def put_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials) and check_user_id(user_id, db, credentials):
        username = retrieve_user_by_username(db, user.username)
        if not username:
            if result := update_user(
                db, user_id, {
                    key: value for key, value in user if value
                }
            ):
                return result

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already registered"
    )
