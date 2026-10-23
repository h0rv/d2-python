import sys
import time
from collections.abc import Iterator

import pytest

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


@pytest.fixture(scope="session", autouse=True)
def timer_session_scope() -> Iterator[None]:
    start = time.time()
    sys.stdout.write(f"\nstart: {time.strftime(DATE_FORMAT, time.localtime(start))}\n")

    yield

    finished = time.time()
    sys.stdout.write(
        f"\nfinished: {time.strftime(DATE_FORMAT, time.localtime(finished))}\n"
    )
    sys.stdout.write(f"Total time cost: {finished - start:.3f}s\n")


@pytest.fixture(autouse=True)
def timer_function_scope() -> Iterator[None]:
    start = time.time()
    yield
    sys.stdout.write(f"\nTime cost: {time.time() - start:.3f}s\n")
