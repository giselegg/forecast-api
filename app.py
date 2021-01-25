from datetime import datetime
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status
)
from sqlalchemy.orm import Session

from crud import (
    create_user,
    remove_user,
    retrieve_all_users,
    retrieve_user_by_id,
    retrieve_user_by_username,
    update_user
)
from database import Base, SessionLocal, engine
from schemas import CreateUserSchema, UpdateUserSchema
from services.fetch_forecast import fetch_forecast

app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    """
    Retorna a sessão de conexão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health/")
def alive():
    """
    Check if API is alive

    Return
        dict: timestamp
    """
    return {"timestamp": datetime.now()}


@app.get("/forecast/")
def empty_forecast():
    """
    Raises exception when user doesn't send city name as parameter
    """
    raise HTTPException(status_code=404, detail="You must enter a city")


@app.get("/forecast/{city_name}")
def get_forecast(city_name: str):
    """
    Get forecast by city name

    Parameters
        str: city name

    Return
        dict: response from fetch_forecast service
    """
    try:
        response = fetch_forecast(city_name)
        if not response:
            raise Exception
        return response
    except Exception as e:
        print(e)


@app.get("/users/", status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    if result := retrieve_all_users(db):
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="There are no users registered",
    )


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    if result := retrieve_user_by_id(db, user_id):
        return result

    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not found"
        )

@app.post(
    "/users/", status_code=status.HTTP_201_CREATED,
)
def post_user(
    user: CreateUserSchema, db: Session = Depends(get_db),
):
    username = retrieve_user_by_username(db, user.username)
    if not username:
        return create_user(db, user)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already registered"
    )


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not remove_user(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID not found"
        )


@app.put("/users/{user_id}", status_code=status.HTTP_201_CREATED)
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

