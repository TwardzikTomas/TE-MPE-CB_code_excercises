# system imports
import sys

# third-party imports
import pytest

# local import
from exercise_two.exercise_two import Package


@pytest.fixture
def log_stdout(monkeypatch):
    captured_stdout = dict(stdout="",
                           write_cnt=0)

    def redirected_write(s):
        captured_stdout["stdout"] += s
        captured_stdout["write_cnt"] += 1

    monkeypatch.setattr(sys.stdout, 'write', redirected_write)
    return captured_stdout


@pytest.fixture
def example_structure():
    p1 = Package("pkg1")
    p1.dependencies = [Package("pkg2", depth_level=1), Package("pkg3", depth_level=1)]
    p1.dependencies[0].dependencies = [Package("pkg3", depth_level=2)]
    p2 = Package("pkg2")
    p2.dependencies = [Package('pkg3', depth_level=1)]
    p3 = Package("pkg3")
    package_structure = [p1, p2, p3]
    return package_structure
