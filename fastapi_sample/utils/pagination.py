from typing import Tuple


def pagination(page: int) -> Tuple[int, int]:
    limit: int = 2
    skip: int = limit * (page - 1)
    return limit, skip
