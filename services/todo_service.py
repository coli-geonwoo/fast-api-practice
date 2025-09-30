from exception.exceptions import TodoNotFoundError, UserNotFoundError
from model import UserTable, TodoTable
from schemas.todo_schema import *
from sqlalchemy.orm import Session
from sqlalchemy import select

def _todo_table_to_todo(todo_table: TodoTable) -> Todo:
    return Todo.model_validate(todo_table)


class TodoService:
    def __init__(self):
        pass

    def create_todo(
            self,
            payload: CreateTodoInput,
            user_id: int,
            db: Session
    ) -> Todo:
        user = db.execute(select(UserTable).where(UserTable.id == user_id)).scalar_one_or_none()
        if not user:
            raise UserNotFoundError()

        todo_table = TodoTable(
            title=payload.title,
            description=payload.description,
            owner_id=user.id,
            completed=payload.completed
        )

        db.add(todo_table)
        db.commit()
        db.refresh(todo_table)
        return _todo_table_to_todo(todo_table)

    def get_todo(
            self,
            key: int,
            user_id: int,
            db: Session
    ) -> Todo:
        todo_table = db.execute(
            select(TodoTable).where(TodoTable.id == key, TodoTable.owner_id == user_id)).scalar_one_or_none()

        if not todo_table:
            raise TodoNotFoundError()
        return _todo_table_to_todo(todo_table)

    def get_all_todos(self, user_id: int, db: Session) -> List[Todo]:
        all_todo_tables = db.execute(select(TodoTable).where(TodoTable.owner_id == user_id)).scalars().all()
        return [_todo_table_to_todo(table) for table in all_todo_tables]

    def update_todo(
            self,
            payload: UpdateTodoInput,
            user_id: int,
            db: Session
    ) -> Todo:
        todo_table = db.execute(
            select(TodoTable).where(TodoTable.id == payload.id, TodoTable.owner_id == user_id)).scalar_one_or_none()

        if not todo_table:
            raise TodoNotFoundError()

        changes = payload.model_dump(exclude_unset=True) # 예상치 못한 값이 있어도 유지하여라
        for key, value in changes.items():
            setattr(todo_table, key, value)

        db.add(todo_table)
        db.commit()
        db.refresh(todo_table)
        return _todo_table_to_todo(todo_table)

    def delete_todo(
            self,
            key: int,
            user_id: int,
            db: Session
    ):
        todo_table = db.execute(
            select(TodoTable).where(TodoTable.id == key, TodoTable.owner_id == user_id)).scalar_one_or_none()

        db.delete(todo_table)
        db.commit()

todo_service = TodoService()


def get_todo_service() -> TodoService:
    return todo_service
