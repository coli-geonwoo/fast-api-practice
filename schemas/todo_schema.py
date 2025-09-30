from pydantic import BaseModel
from typing import Optional, List
from validator.todo_validator import *

from pydantic import Field, field_validator, ConfigDict



class Todo(BaseModel):
    id: int
    title: TitleRule
    description: OptionalDescriptionRule
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateTodoInput(BaseModel):
    id: int
    title: TitleRule
    description: OptionalDescriptionRule
    completed: bool = False


class CreateTodoInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(None, min_length=1, max_length=2000)
    completed: bool = False

    @field_validator("title", mode = "before")
    @classmethod
    def validate(cls, value):
        #검증로직 작성
        return value

    @field_validator("description", mode = "before")
    @classmethod
    def validate2(cls, value):
        # 검증로직 작성
        return value