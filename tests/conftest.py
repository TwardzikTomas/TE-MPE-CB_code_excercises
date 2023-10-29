# system imports
import sys


# third-party imports
import pytest


@pytest.fixture
def log_stdout(monkeypatch):
    captured_stdout = dict(stdout="",
                           write_cnt=0)

    def redirected_write(s):
        captured_stdout["stdout"] += s
        captured_stdout["write_cnt"] += 1

    monkeypatch.setattr(sys.stdout, 'write', redirected_write)
    return captured_stdout
