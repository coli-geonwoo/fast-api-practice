from auth.auth_bearer import JWTBearer
from db import get_db_session
from services.todo_service import *
from fastapi import FastAPI, Depends, status, APIRouter

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    dependencies=[Depends(JWTBearer)]
)


@router.post(
    "/",  # POST /
    response_model=Todo,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    summary="Create a new todo")
def create_todo(
        payload: CreateTodoInput,
        user_id: str = Depends(JWTBearer()),
        service: TodoService = Depends(get_todo_service),
        db: Session = Depends(get_db_session)
) -> Todo:
    todo_out = service.create_todo(payload=payload, user_id=int(user_id), db=db)
    return todo_out


@router.get(
    "/todos/all",
    response_model=List[Todo]
)
def find_todo(
        user_id: str = Depends(JWTBearer()),
        service: TodoService = Depends(get_todo_service),
        db: Session = Depends(get_db_session)

) -> List[Todo]:
    return service.get_all_todos(user_id=int(user_id), db=db)


@router.get(
    "/todos/{todo_id}",
    response_model=Todo
)
def find_todo(
        todo_id: int,
        user_id: str = Depends(JWTBearer()),
        service: TodoService = Depends(get_todo_service),
        db: Session = Depends(get_db_session)
) -> Todo:
    return service.get_todo(key=todo_id, user_id=int(user_id), db=db)


@router.patch(
    "/",  # POST /
    response_model=Todo,
)
def update_todo(
        payload: UpdateTodoInput,
        user_id: str = Depends(JWTBearer()),
        service: TodoService = Depends(get_todo_service),
        db: Session = Depends(get_db_session)
) -> Todo:
    todo_out = service.update_todo(payload=payload, user_id=int(user_id), db=db)
    return todo_out


@router.delete(
    "/{todo_id}",  # POST /
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo(
        todo_id: int,
        user_id: str = Depends(JWTBearer()),
        service: TodoService = Depends(get_todo_service),
        db: Session = Depends(get_db_session)
):
    service.delete_todo(key=todo_id, user_id=int(user_id), db=db)
