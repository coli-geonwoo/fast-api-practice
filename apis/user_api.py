from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from db import get_db_session
from schemas.user_schema import *
from services.user_service import get_user_service, UserService
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.post(
    "",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    summary="Create a new user",
)
def create_user(
    payload: CreateUserInput,
    service : UserService = Depends(get_user_service),
    db: Session = Depends(get_db_session)
) -> UserOut:
    user = service.create_user(payload =payload, db=db)
    user_out = UserOut(
        id = user.id,
        name = user.name,
        todo_id_list= user.todo_id_list
    )
    return user_out


@router.get(
    "/me",
    response_model=UserWithTokenOutput,
    summary="Get user information",
    dependencies = [Depends(JWTBearer())]
)
def get_user(
        user_id : str = Depends(JWTBearer()),
        user_service : UserService = Depends(get_user_service),
        db: Session = Depends(get_db_session)
) -> UserWithTokenOutput:
    user = user_service.get_user(int(user_id), db=db)
    user_out = UserOut(
        id=user.id,
        name=user.name,
        todo_id_list=user.todo_id_list
    )
    access_token = signJWT(user_id)
    return UserWithTokenOutput(user= user_out, access_token= access_token)


@router.post(
    "/login",
    response_model=UserWithTokenOutput,
    summary="Login a user",
)
def login_user(
    payload: LoginUserInput,
    user_service : UserService = Depends(get_user_service),
    db: Session = Depends(get_db_session)
) -> UserWithTokenOutput:
    user = user_service.login_user(payload, db=db)
    user_out = UserOut(
        id=user.id,
        name=user.name,
        todo_id_list=user.todo_id_list
    )
    access_token = signJWT(user.id)
    return UserWithTokenOutput(user = user_out, access_token = access_token)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    dependencies=[Depends(JWTBearer())]
)
def delete_user(
        user_id: str = Depends(JWTBearer()),
        user_service: UserService = Depends(get_user_service),
        db: Session = Depends(get_db_session)
) -> None:
    user_service.delete_user(int(user_id), db=db)