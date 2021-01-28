
from fastapi import HTTPException, status
from secrets import compare_digest

from crud.users import retrieve_user_by_username, retrieve_user_by_id


def check_authorization(db, credentials):
    db_user = retrieve_user_by_username(db, credentials.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    correct_username = compare_digest(credentials.username, db_user.username)
    correct_password = compare_digest(credentials.password, db_user.password)

    if correct_username and correct_password:
        return True
    return False


def check_user_id(user_id, db, credentials):
    db_user = retrieve_user_by_username(db, credentials.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if user_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="It's not possible to access another user's account",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True
