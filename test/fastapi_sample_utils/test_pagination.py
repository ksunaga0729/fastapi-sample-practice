from fastapi_sample.utils.pagination import pagination


def test_pagination():
    page = pagination(2)
    assert page == (2, 2)
