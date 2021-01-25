from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class CreateUserSchema(UserBaseSchema):
    password: str


class UpdateUserSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True