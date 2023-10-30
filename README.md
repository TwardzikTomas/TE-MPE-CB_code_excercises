# TE-MPE-CB_code_exercises

![Tests](https://github.com/TwardzikTomas/TE-MPE-CB_code_excercises/actions/workflows/python-package.yml/badge.svg)

## Overview
Temporary repository, showcasing my proposed solution for CERN's Controls and Beam section entry coding exam using Python programming language.

## Structure
This repository solves both exercises. The solutions are provided in directory ***solutions***. Exercise one is solved in a module **exercise_one**, while the exercise two is solved in package **exercise_two**. Tests for the second task are located in directory ***tests***, with set of provided JSON files showcasing used to demonstrate expected behavior.  

The project requires multiple configuration files to make testing, GitHub actions and package building work. We have namely:
- **setup.py**, **setup.cfg** and **pyproject.toml** to set up building of the package, configuration of MyPy, Flake8 linter and PyTest suite,
- **requirements.txt** and **requirements_dev.txt** to define package dependencies for building and testing respectively,
- **.github/workflows** holding automated CI action for testing.

## Solution

### Exercise one

### Exercise two

## Entry points

## Test suite
The project runs following testing adn QA tools: static type checker **MyPy**, code linter **Flake8** and code unit testing through **PyTest**. 

Required dependencies for execution of tests are listed in **requirements_dev.txt**.

### MyPy
Triggering **MyPy** on **solutions** can be done with a command:
```python
mypy solutions
```
Configuration of the **MyPy** is located in **pyproject.toml**. As one can notice, option *disallow_any_generics* is not selected, however this is intentional, as **exercise_one** can accept a list of generic content and thereby this option is allowed.

### Flake8
To execute Python linter **Flake8** on ***solutions** run:

```
flake8 solution
```

**Flake8** is configured in **setup.cfg**. This project is configured to 'max-line-length' of 160 characters.

### PyTest

Unit testing is covered with **PyTest** library. Test are, as requested, only available for the second exercise. Testing is located within folder ***tests***, where file **test_exercise_two.py** holds defined tests, file **conftest.py** has helping test fixtures and folder ***test_jsons*** contains examples of JSON files used for testing purposes.

The unit test suite can be executed with:

```
pytest
```

At this moment, test suite consists of 20 tests, all of which are passing.

**PyTest** is configured under **pyproject.toml** file, and runs only one package **exercise_two** and produces a PyTest coverage report with missing lines listed.

### Protected main branch
This repository has protected ***main*** branch. This means that to push in it, one needs to create a *pull request*, that then needs to be approved by an administrator. 

Furthermore, one needs to pass all CI tests in a **feature** branch (or any other arbitrarily named branch) before being able to merge and push to the ***main*** branch. Also, one needs to have both the **feature** and ***main*** branch up to date before merging is enabled.

More about protected branches can be read ![here.](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
