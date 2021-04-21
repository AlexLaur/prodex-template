import re
import pathlib


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def parts_matching(path, definitions):
    """Check if the given path path has the minimum required parts to fit
    with the template.

    >>> path = "/prod/projects/foo/bar" # length parts: 4
    >>> definitions = [
    ... "/prod/project/{var_a}/bar", # length parts: 4
    ... "/prod/project/{var_a}/{var_b}/bar", # length parts: 5
    ... ]
    >>> parts_matching(path, definitions)
    >>> True

    :param path: The path to analyse
    :type path: str
    :param definitions: All possible definitions for the path
    :type definitions: list
    :return: True if only one match is found, False if not.
    :rtype: bool
    """
    matching = False
    path = pathlib.Path(path)
    for definition in definitions:
        definition = pathlib.Path(definition)
        if len(list(path.parts)) != len(list(definition.parts)):
            continue
        matching = True
    return matching


def find_placeholder(path):
    """Find all placeholders in the given path

    >>> path = "/prod/projects/{foo}/{bar}/"
    >>> find_placeholder(path=path)
    >>> ["foo", "bar"]

    :param path: The path to analyse.
    :type path: str
    :return: List of all placeholders which have been found.
    :rtype: list
    """
    return re.findall(r"{(\w+)}", path)


def paths_categorization(paths):
    root_paths = {}
    other_paths = {}
    for key, path in paths.items():
        if isinstance(path, dict):
            # The path have a definition or root_name keys
            other_paths[key] = path
            continue
        root_paths[key] = pathlib.Path(path)
    return other_paths, root_paths


def remove_root_paths_from_paths(paths, root_paths):
    for root in root_paths:
        paths.pop(root)
    return paths


def sanitize_link(link):
    return link.strip().partition(".")[0]
