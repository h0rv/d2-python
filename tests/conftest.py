import time

import pytest


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


@pytest.fixture(scope="session", autouse=True)
def timer_session_scope():
    start = time.time()
    print(f"\nstart: {time.strftime(DATE_FORMAT, time.localtime(start))}")

    yield

    finished = time.time()
    print(f"\nfinished: {time.strftime(DATE_FORMAT, time.localtime(finished))}")
    print(f"Total time cost: {finished - start:.3f}s")


@pytest.fixture(autouse=True)
def timer_function_scope():
    start = time.time()
    yield
    print(f"\nTime cost: {time.time() - start:.3f}s")
