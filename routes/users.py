
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status
)
from sqlalchemy.orm import Session

from crud.users import (
    create_user,
    retrieve_all_users,
    retrieve_user_by_id,
    retrieve_user_by_username,
    update_user,
    remove_user
)
from database import Base, SessionLocal, engine
from schemas.users import CreateUserSchema, UpdateUserSchema


# Database
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Returns DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
users_router = APIRouter(prefix="/users")

@users_router.get("", status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    if result := retrieve_all_users(db):
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="There are no users registered",
    )


@users_router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    if result := retrieve_user_by_id(db, user_id):
        return result

    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not found"
        )


@users_router.post("", status_code=status.HTTP_201_CREATED)
def post_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    username = retrieve_user_by_username(db, user.username)
    if not username:
        return create_user(db, user)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already registered"
    )


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if remove_user(db, user_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User ID not found"
    )


@users_router.put("/{user_id}", status_code=status.HTTP_201_CREATED)
def put_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(get_db)):
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
