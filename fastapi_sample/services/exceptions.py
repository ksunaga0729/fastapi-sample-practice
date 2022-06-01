class NotFoundException(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message


class ConflictException(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message


class ForbiddenException(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
