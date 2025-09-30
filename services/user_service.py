from exception.exceptions import UserNotFoundError, LoginFailedError, UserAlreadyExistsError
from schemas.user_schema import User, LoginUserInput, CreateUserInput
from sqlalchemy.orm import Session
from sqlalchemy import select, exists
from model import UserTable, TodoTable
from typing import Optional
from fastapi.exceptions import HTTPException


def _get_user_todo_list(db: Session, user_id: int) -> list[int]:
    todo_id_sequence = db.execute(select(TodoTable.id).where(TodoTable.owner_id == user_id)).scalars().all()
    return list(todo_id_sequence)


def _convert_to_user(row: UserTable, *, db: Session | None = None, with_todo_ids: bool = True) -> User:
    todo_ids : list[int] = []
    if with_todo_ids and db is not None:
        todo_ids = _get_user_todo_list(db, row.id)
    return User(id=row.id, name=row.name, password=row.password, todo_id_list=todo_ids)


class UserService:

    def __init__(self):
        self.database: dict[int, User] = {}
        self.counter: int = 1

    def create_user(
            self,
            payload: CreateUserInput,
            db: Session
    ) -> User:
        user_table = db.execute(select(UserTable).where(UserTable.name == payload.name)).scalar_one_or_none()

        if user_table:
            raise UserAlreadyExistsError()

        user_table = UserTable(
            name=payload.name,
            password=payload.password
        )
        db.add(user_table)
        db.commit()
        db.refresh(user_table)
        return _convert_to_user(user_table)

    def get_user(
            self,
            user_id: int,
            db: Session
    ) -> User:
        found_user_table = db.execute(select(UserTable).where(UserTable.id == user_id)).scalar_one_or_none()

        if not found_user_table:
            raise UserNotFoundError()
        return _convert_to_user(found_user_table)

    def login_user(
            self,
            payload: LoginUserInput,
            db: Session
    ) -> User:
        found_user_table = db.execute(select(UserTable)
                                      .where(UserTable.name== payload.name,
                                             UserTable.password == payload.password)
                                      ).scalar_one_or_none()
        if not found_user_table:
            raise LoginFailedError()
        return _convert_to_user(found_user_table)

    def delete_user(self, user_id: int, db: Session) -> None:
        found_user_table = db.execute(select(UserTable).where(UserTable.id == user_id)).scalar_one_or_none()

        db.delete(found_user_table)
        db.commit()


user_service = UserService()


def get_user_service():
    return user_service
