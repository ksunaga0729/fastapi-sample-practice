import invoke


@invoke.task
def lint(c):
    """
    ソースコードのフォーマット及び静的解析を行います
    """
    c.run("isort fastapi_sample test")
    c.run("black fastapi_sample test")
    c.run("flake8 fastapi_sample test")
    c.run("mypy fastapi_sample test")
