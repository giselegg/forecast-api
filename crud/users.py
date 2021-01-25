from sqlalchemy.orm import Session

from models.users import Users
from schemas.users import CreateUserSchema, UpdateUserSchema

users = Users


def create_user(db: Session, user: CreateUserSchema):
    new_user = Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def retrieve_all_users(db: Session):
    return db.query(users).all()


def retrieve_user_by_id(db: Session, user_id: int):
    return db.query(users).filter(users.id == user_id).first()


def retrieve_user_by_username(db: Session, username: str):
    return db.query(users).filter(users.username == username).first()


def update_user(db: Session, user_id: int, values: UpdateUserSchema):
    if user := retrieve_user_by_id(db, user_id):
        db.query(users).filter(users.id == user_id).update(values)
        db.commit()
        db.refresh(user)

        return user


def remove_user(db: Session, user_id: int):
    if user := retrieve_user_by_id(db, user_id):
        db.delete(user)
        db.commit()
        return True

    return False
