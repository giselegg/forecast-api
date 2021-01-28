
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
from services.auth import check_authorization, check_user_id, check_username
from services.logger import RequestLogger


# Logger
logger = RequestLogger(__name__, "requests.log").logger

# Security
security = HTTPBasic()

# Routes
users_router = APIRouter(prefix="/users")


@users_router.get("", status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials):
        if result := retrieve_all_users(db):
            logger.info(f"username: {credentials.username}, request: get all users")
            return result

    raise HTTPException(
        status_code=400,
        detail="Username or password incorrect"
    )


@users_router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials) and check_user_id(user_id, db, credentials):
        if result := retrieve_user_by_id(db, user_id):
            logger.info(f"username: {credentials.username}, request: get user")
            return result

    raise HTTPException(
        status_code=400,
        detail="Username or password incorrect"
    )


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials) and check_user_id(user_id, db, credentials):
        if remove_user(db, user_id):
            logger.info(f"username: {credentials.username}, request: remove user")
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=400,
        detail="Username or password incorrect"
    )


@users_router.put("/{user_id}", status_code=status.HTTP_201_CREATED)
def put_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials) and check_user_id(user_id, db, credentials) and check_username(db, user, credentials):
        if result := update_user(
            db, user_id, {
                key: value for key, value in user if value
            }
        ):
            logger.info(f"username: {credentials.username}, request: update user")
            return result


    raise HTTPException(
        status_code=400,
        detail="Username or password incorrect"
    )
