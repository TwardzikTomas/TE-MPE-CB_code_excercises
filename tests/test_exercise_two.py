# system imports
from os.path import dirname, abspath, join
import json

# local imports
from exercise_two.exercise_two import (CyclicImportError, MissingPackageError, Package, DependencyResolver,
                                       show_dependency_graph, build_dependency_graph)

# third-party imports
import pytest


# helper function
def add_test_path(file_name: str):
    return join(dirname(abspath(__file__)), "test_jsons", file_name)


def test_package_eq():
    package_name = 'pkg'
    depth = 2
    p1 = Package(package_name, depth_level=depth)
    p2 = Package(package_name, depth_level=depth)
    assert p1 == p2


@pytest.mark.parametrize('test_name, test_dependency_flag,test_depth',
                         [('pkg2', True, 0),
                          ('pkg', True, 1),
                          ('pkg', False, 2),
                          ])
def test_package_noteq(test_name, test_dependency_flag, test_depth):
    dep_p = Package('dep_pkg', depth_level=3)
    p1 = Package('pkg', depth_level=2)
    p1.dependencies = [dep_p]
    p2 = Package(test_name, test_depth)
    if test_dependency_flag is True:
        p2.dependencies = [dep_p]
    assert p1 != p2


def test_package_eq_type_mismatch():
    p1 = Package('pkg', depth_level=2)
    assert p1 != 'package'


def test_package_repr(log_stdout):
    p1 = Package('pkg', depth_level=2)
    print(p1)
    assert log_stdout["stdout"] == "Package(name='pkg', dependencies=[], depth_level=2)\n"


