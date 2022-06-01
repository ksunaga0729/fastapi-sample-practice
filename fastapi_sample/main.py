import uvicorn  # type: ignore
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from fastapi_sample.services import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
)

from .routers import authentication, messages, rooms, users, users_rooms

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(messages.router)
app.include_router(rooms.router)
app.include_router(users_rooms.router)


@app.exception_handler(NotFoundException)
async def notfound_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


@app.exception_handler(ForbiddenException)
async def fodidden_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=403,
        content={"message": exc.message},
    )


@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=409,
        content={"message": exc.message},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
