from __future__ import annotations
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db_base import db_base

class UserTable(db_base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index= True, autoincrement=True)
    name = Column(String, index=True, unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    todos = relationship(
        "TodoTable",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy= "noload",
        passive_deletes = True,
        order_by = "TodoTable.id"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, data: dict) -> UserTable:
        return cls(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # "password": self.password,  # 보안상 제외
        }

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"