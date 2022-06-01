from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

SECRET_KEY = config("SECRET_KEY", cast=Secret)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=7 * 24 * 60
)
