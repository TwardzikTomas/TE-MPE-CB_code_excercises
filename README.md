# TE-MPE-CB_code_exercises

![Tests](https://github.com/TwardzikTomas/TE-MPE-CB_code_excercises/actions/workflows/python-package.yml/badge.svg)

## Overview
Temporary repository, showcasing my proposed solution for CERN's Controls and Beam section entry coding exam using Python programming language.

## Structure
This repository solves both exercises. The solutions are provided in directory ```solutions```. Exercise one is solved in a module ***exercise_one***, while the exercise two is solved in package ***exercise_two***. Tests for the second task are located in directory ```tests```, with a set of provided JSON files used to demonstrate expected behavior.  

The project requires multiple configuration files to make testing, GitHub actions and package building work. Namely, we have:
- **setup.py**, **setup.cfg** and **pyproject.toml** to set up building of the package, configuration of MyPy, Flake8 linter and PyTest suite,
- **requirements.txt** and **requirements_dev.txt** to define package dependencies for building and testing, respectively,
- **.github/workflows** holding automated CI action for testing.

## Installing the package
After cloning the repository, one needs to set up an environment and install the package. It is required to use Python>3.9 for this package.

Installation can be done by:
```
pip install -r requirements.txt .
```
or in editable mode with:
```
pip install -r requirements.txt -e .
```

>Editable mode enables ```click``` based entrypoints (commands `detect-duplicates` and `show-dependency`). If you want to use these two commands, you are obligated to install in editable mode.

## Entry points
For convenience, user can access some code functionality directly from the command line interface.

For module ***exercise_one***, one can use `click` CLI, accessed by:
```
detect-duplicates <args>, ..., ,<argN>
```

>Limitation: Arguments \<argsX> are type casted into strings, therefore this entrypoint should be used only with strings. 

Example: a poor use of ```detect-duplicates``` entry point:
```
detect-duplicate 1 '1' 
-> ['1']
```
***
For ***exercise_two*** one can run the package with the default path (```/tmp/deps.json```) as:
```
python -m exercise_two
```
Which produces expected output:
```
- pkg1
  - pkg2
    - pkg3
  - pkg3
- pkg2
  - pkg3
- pkg3
```
User defined target path for dependency graph plot is exposed through command:

```
show-dependency -f <absolute_path>
```
Invoking the command without the `-f` option gives the default behavior mentioned above.

***
Entry points are defined in the config file **setup.cfg**, and implementation of ```click``` CLI is in the located at ```/solutions/entry_points.py```. Commands defined with ```click``` have `--help` flags implemented to inspect their syntax and arguments.

Both exercises can be also accessed normally,as modules, unlocking finer and less limiting interaction.

## Test suite
The project runs following testing and QA tools: static type checker **MyPy**, code linter **Flake8** and code unit testing through **PyTest**. 

Required dependencies for execution of tests are listed in **requirements_dev.txt**.

### MyPy
Triggering **MyPy** on ```solutions``` can be done with a command:
```python
mypy solutions
```
Configuration of the **MyPy** is located in **pyproject.toml**. As one can notice, option *disallow_any_generics* is not selected, however, this is intentional, as ***exercise_one*** can accept a list of generic content and thereby this option is allowed.

### Flake8
To execute Python linter **Flake8** on ```solutions``` run:

```
flake8 solutions
```

**Flake8** is configured in **setup.cfg**. This project is configured to 'max-line-length' of 160 characters.

### PyTest

Unit testing is covered with **PyTest** library. Test are, as requested, only available for the second exercise. Testing is located within folder ```tests```, where file **test_exercise_two.py** holds defined tests, file **conftest.py** has helping test fixtures and folder ```test_jsons``` contains examples of JSON files used for testing purposes.

The unit test suite can be executed with:

```
pytest
```

At this moment, test suite consists of 19 tests, all of which are passing.

**PyTest** is configured under **pyproject.toml** file, and runs only one package ***exercise_two*** and produces a PyTest coverage report with missing lines listed.

### Protected main branch
This repository has protected ***main*** branch. This means that to push in it, one needs to create a *pull request*, that then needs to be approved by an administrator. 

Furthermore, one needs to pass all CI tests in a **feature** branch (or any other arbitrarily named branch) before being able to merge and push to the ***main*** branch. Also, one needs to have both the **feature** and ***main*** branch up to date before merging is enabled.

More about protected branches can be read [here](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
