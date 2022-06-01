import tempfile

import pytest
from factory.alchemy import SQLAlchemyModelFactory
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import EmailStr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.config import Config

from fastapi_sample import models
from fastapi_sample.cruds import UserRepository
from fastapi_sample.dependencies.database import get_session
from fastapi_sample.schemas import user as user_schema

from .utils.utils import create_token_header

config = Config(".env")


@pytest.fixture
def app() -> FastAPI:
    from fastapi_sample import main

    return main.app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture()
def engine():
    tfile = tempfile.NamedTemporaryFile()
    url = "sqlite:///" + tfile.name

    return create_engine(url, connect_args={"check_same_thread": False})


@pytest.fixture()
def session(engine):
    models.Base.metadata.create_all(bind=engine)

    Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    session = Session()

    yield session

    session.close()


@pytest.fixture(autouse=True)
def mock_dependency(app, session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def test_user(session: Session) -> models.User:
    new_user = user_schema.UserCreate(
        email=EmailStr("yamada@example.com"),
        username="Yamada",
        password="password",
    )
    user_repo = UserRepository(session)
    existing_user = user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return user_repo.create_user(new_user)


@pytest.fixture
def token_header(client: TestClient, test_user):
    return create_token_header(client, test_user)


@pytest.fixture
def factory(session):
    class Factory:
        class BaseFactory(SQLAlchemyModelFactory):
            class Meta:
                sqlalchemy_session = session
                sqlalchemy_session_persistence = "commit"

        class User(BaseFactory):
            class Meta:
                model = models.User

            password = "password"

        class Message(BaseFactory):
            class Meta:
                model = models.Message

        class Room(BaseFactory):
            class Meta:
                model = models.Room

        class Member(BaseFactory):
            class Meta:
                model = models.Member

            member_role = "general"

        class Thread(BaseFactory):
            class Meta:
                model = models.Thread

    return Factory
