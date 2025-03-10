"""
This type stub file was generated by pyright.
"""

import pytest
from contextlib import contextmanager
from numpy.testing._private.utils import NOGIL_BUILD

"""
Pytest configuration and fixtures for the Numpy test suite.
"""
HAVE_SCPDT = ...
_old_fpu_mode = ...
_collect_results = ...
_pytest_ini = ...
def pytest_configure(config): # -> None:
    ...

def pytest_addoption(parser): # -> None:
    ...

gil_enabled_at_start = ...
if NOGIL_BUILD:
    gil_enabled_at_start = ...
def pytest_sessionstart(session): # -> None:
    ...

def pytest_terminal_summary(terminalreporter, exitstatus, config): # -> None:
    ...

@pytest.hookimpl()
def pytest_itemcollected(item): # -> None:
    """
    Check FPU precision mode was not changed during test collection.

    The clumsy way we do it here is mainly necessary because numpy
    still uses yield tests, which can execute code at test collection
    time.
    """
    ...

@pytest.fixture(scope="function", autouse=True)
def check_fpu_mode(request): # -> Generator[None, Any, None]:
    """
    Check FPU precision mode was not changed during the test.
    """
    ...

@pytest.fixture(autouse=True)
def add_np(doctest_namespace): # -> None:
    ...

@pytest.fixture(autouse=True)
def env_setup(monkeypatch): # -> None:
    ...

@pytest.fixture(params=[True, False])
def weak_promotion(request): # -> Generator[Any, Any, None]:
    """
    Fixture to ensure "legacy" promotion state or change it to use the new
    weak promotion (plus warning).  `old_promotion` should be used as a
    parameter in the function.
    """
    ...

if HAVE_SCPDT:
    @contextmanager
    def warnings_errors_and_rng(test=...): # -> Generator[None, Any, None]:
        """Filter out the wall of DeprecationWarnings.
        """
        ...
    
