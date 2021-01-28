from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.users import create_user, retrieve_user_by_username
from database.config import Base, SessionLocal, engine
from database.get_db import get_db
from schemas.users import CreateUserSchema

# Database
Base.metadata.create_all(bind=engine)
get_db()


# Routes
register_router = APIRouter(prefix="/register")

@register_router.post("", status_code=status.HTTP_201_CREATED)
def post_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    username = retrieve_user_by_username(db, user.username)
    if not username:
        return create_user(db, user)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already registered"
    )
