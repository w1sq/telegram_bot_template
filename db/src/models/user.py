from typing import Optional

from sqlmodel import Field

from .base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    username: Optional[str] = Field(max_length=32, default=None)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    is_staff: bool = Field(default=False)

    def is_admin(self) -> bool:
        return self.is_staff

    def is_user(self) -> bool:
        return not self.is_staff
