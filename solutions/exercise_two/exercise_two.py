"""
Write a small program, which:

 Reads a JSON file from a fixed filesystem location, e.g. /tmp/deps.json, containing a list of packages and their dependencies.
 In this JSON file, a key represents a package name, and the value is a list of dependencies (package names) for that key:

'{
  "pkg1": ["pkg2", "pkg3"],
  "pkg2": ["pkg3"],
  "pkg3": []
}'

Traverses the dependencies loaded from the JSON file and reconstructs the full dependency graph.
For the input above, the full graph would be the following:

- pkg1
  - pkg2
    - pkg3
  - pkg3
- pkg2
  - pkg3
- pkg3

Has a function that takes a filename as an input and returns an object representing the fully resolved graph.
Please provide a test case that validates this function. Use any testing framework of your choice.

Is a valid Python package or module and is runnable with python -m program_name command. 
Running this command should print the graph to stdout. The format in which it prints is not important.

In addition, setup a CI pipeline (using Gitlab CI, Github Actions or equivalent)to ensure the best possible automation for the quality of your code.


assumptions:
	- format of the dependency json file is as given
	- 
"""

# WARNING pozor na nedefinovane dependencies, mam jen ve strome ale nemam tu dependency available
# pozor na cyclic dependencies

# system imports
import os
from json import load
from typing import Union
from pathlib import Path

# custom type hints definition
dependency_tree = dict[str, dict]

# global variables
TARGET_PATH = "/tmp/deps.json"

class CyclicImportError(Exception):
    ...
    
class MissingPackageError(Exception):
    ...

class Package:
    def __init__(self, name: str, dependencies:list['Package']= None, depth_level: int = 0):
        self.name = name
        self.dependencies = dependencies
        self.depth_level = depth_level


class DependencyResolver:    
    def verify_dependency_structure(self, dependency_data: dict[str, list]) -> None:
        self.verify_presence(dependency_data)
        self.verify_cyclic_imports(dependency_data)        
        

# TODO ? mozna prepsat a spojit do jednoho? + perforamce -extendibility, readability
    def verify_presence(self, dependency_data: dict[str, list]) -> bool:
        pkgs = dependency_data.keys()
        for _, deps in dependency_data.items():
            for dep in deps:
                if dep not in pkgs:
                    raise MissingPackageError(f"ERROR: Package {dep!r} was not found in dependency list")


    def verify_cyclic_imports(self, dependency_data: dict[str, list]):
        for pkg, deps in dependency_data.items():
            for dep in deps:
                if pkg in dependency_data[dep]:
                    raise CyclicImportError(f"ERROR: packages {pkg!r} and {dep!r} are creating cyclic dependency")
 
    
    @classmethod
    def resolve_graph(cls, file_path: Union[str, Path]) -> dependency_tree:
        def resolve_dependency(pkg: str):
            print(f"resolve dependency {pkg=}")
            dependencies = {}
            
            if len(dependency_data[pkg]) == 0:
                print("returning empty as the package is independent")
            else:
                try:
                    for dependency in dependency_data[pkg]:
						# print(f"gooing deeper with recursion: from {pkg=} looking for deps of {dependency}")
                        dependencies[f"{dependency}"] = resolve_dependency(dependency)
                except KeyError:
                    print(f"Dependency {dependency} is missing in the {file_path}")
        
            print(f"returning dependencies of {pkg}: {dependencies}")
            return dependencies
		
		# check for existence of a file, shortcircuit for errors
        if os.path.isfile(file_path) is False:
            raise FileExistsError(f"Error. File at the path {file_path} does not exist.")

        dependency_data = {}
        with open(file_path) as json_file:
            dependency_data: dict = load(json_file)
   
        print(f"{dependency_data=}")
        
        try:
            cls.verify_dependency_structure(dependency_data)
        except Exception:
            print("Aborting program due to data structure issues")
            quit(-1)
            
        else:
            dependency_dict = {}
            for pkg in dependency_data.keys():
                dependency_dict[f"{pkg}"] = resolve_dependency(pkg)
                
            return dependency_dict

  
    @classmethod
    def print_graph(cls, file_path: Union[str, Path]):
        resolved_graph = cls.resolve_graph(file_path)

        print(f"{resolved_graph}")
	
  
if __name__ == "__main__":
	
	dr = DependencyResolver()
	dr.resolve_graph(TARGET_PATH)
	dr.print_graph(TARGET_PATH)