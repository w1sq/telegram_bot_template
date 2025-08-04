from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy.types import BigInteger


class BaseModel(SQLModel):

    id: Optional[int] = Field(default=None, primary_key=True, sa_type=BigInteger)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
