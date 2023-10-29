"""
Default setuptools entry point does not allow for argument, so one needs to use argparse similar. I prefer 'click'.
"""

from exercise_two.exercise_two import show_dependency_graph, TARGET_PATH
from exercise_one.exercise_one import detect_duplicate_elements
import click


@click.command()
@click.option("-f", "--file_path",
              default=TARGET_PATH,
              show_default=True,
              type=str,
              help="Defines absolute path to a JSON file containing dependency relations.")
def dependency_graph(file_path):
    show_dependency_graph(file_path)


@click.command()
@click.argument('elements', nargs=-1)
def detect_duplicate(elements):
    print(detect_duplicate_elements(elements))
