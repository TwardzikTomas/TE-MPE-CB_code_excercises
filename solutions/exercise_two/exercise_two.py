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
	- valid format of the dependency json file is as given
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
    """
    Raised if cyclic dependency is detected during verification of the dependency file file
    """
    ...
    
class MissingPackageError(Exception):
    """
    Raised if a missing package is detected during verification of the dependency file
    """
    ...

class Package:
    """Class that represents a package, with its dependencies and depth in the dependency graph
    """
    def __init__(self, name: str, depth_level: int = 0):
        self.name = name
        self.dependencies: list['Package'] = []
        self.depth_level = depth_level
        
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name!r}, dependencies={[dependency.name for dependency in self.dependencies]}, depth_level={self.depth_level!r})"
            
    def structural_print(self):
        """
        Convenience method that recursively prints dependency structure of a package
        """
        print(f"{self.depth_level*'  '}- {self.name}")
        for dep in self.dependencies:
            dep.structural_print()

class DependencyResolver:  
      
    def verify_dependency_structure(self, dependency_data: dict[str, list]) -> None:
        self.verify_dependency_fields(dependency_data)     
        self.verify_presence(dependency_data)
        self.verify_cyclic_imports(dependency_data)   
        
    def verify_dependency_fields(self, dependency_data: dict[str, list]) -> None:
        if not isinstance(dependency_data, dict):
            raise TypeError(f"Loaded JSON file does not provide dictionary")
        for pkg, deps in dependency_data.items():
            if not isinstance(pkg, str):
                raise TypeError(f"ERROR: Package name {pkg!r} is not string")
            if not isinstance(deps, list):
                raise TypeError(f"ERROR: Package {pkg!r} dependencies are not a list")

    def verify_presence(self, dependency_data: dict[str, list]) -> None:
        pkgs = dependency_data.keys()
        for _, deps in dependency_data.items():
            for dep in deps:
                if dep not in pkgs:
                    raise MissingPackageError(f"ERROR: Package {dep!r} was not found in dependency list")


    def verify_cyclic_imports(self, dependency_data: dict[str, list]) -> None:
        for pkg, deps in dependency_data.items():
            for dep in deps:
                if pkg in dependency_data[dep]:
                    raise CyclicImportError(f"ERROR: packages {pkg!r} and {dep!r} are creating cyclic dependency")
 
    def resolve_graph(self, file_path: Union[str, Path]) -> list[Package]:
        def resolve_dependency(pkg: str, depth:int=0):
            
            package = Package(pkg, depth)
            
            if len(dependency_data[pkg]) != 0:
                for dependency in dependency_data[pkg]:
                    # print(f"gooing deeper with recursion: from {pkg=} looking for deps of {dependency}")
                    package.dependencies.append(resolve_dependency(dependency, depth+1))
            # print(f"returning  of {pkg}: {package}")
            return package
		
		# check for existence of a file, shortcircuit for errors
        if os.path.isfile(file_path) is False:
            raise FileExistsError(f"Error. File at the path {file_path} does not exist.")

        
        with open(file_path) as json_file:
            dependency_data: dict = load(json_file)
   
        try:
            self.verify_dependency_structure(dependency_data)
        except (MissingPackageError, CyclicImportError):
            print("Aborting program due to data structure issues")
            raise
        else:
            dependency_graph = []
            for pkg in dependency_data.keys():
                dependency_graph.append(resolve_dependency(pkg))
                
            return dependency_graph

    def print_dependency_graph(self, file_path: Union[str, Path]) -> None:
        """Prints a formatted dependency graph defined by 'file_path' file

        Args:
            file_path (Union[str, Path]): JSON file containing dependency relations
        """
        resolved_graph = self.resolve_graph(file_path)

        for node in resolved_graph:
            node.structural_print()
	
  
# example uses
if __name__ == "__main__":
	
	dr = DependencyResolver()
    
    # retrieve dependency structure
	package_structure = dr.resolve_graph(TARGET_PATH)
 
    # print dependency graph
	dr.print_dependency_graph(TARGET_PATH)