from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi_sample.config.database import Session as DBSession
from fastapi_sample.cruds.base import BaseRepository

T = TypeVar("T", bound=BaseRepository)


def get_session() -> Session:
    return DBSession()


def get_repository(repo_type: Type[T]) -> Callable:
    def get_repo(db: Session = Depends(get_session)) -> T:
        return repo_type(db)

    return get_repo
