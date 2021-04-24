import pathlib

import yaml

from errors import ProdexTemplateCircular


def get_include_as_absolute_path(file_name, include):
    """Return the absolute path of any includes in the config file

    :param file_name: The path of the parsed config from wich the include was
    discovered.
    :type file_name: pathlib.Path
    :param include: The include file
    :type include: str
    :return: The absolute path if the file exists, None instead
    :rtype: pathlib.Path
    """
    include_path = pathlib.Path(include)
    if not include_path.is_absolute():
        # The path is not an absolute path, convert it.
        include_path = file_name.parent / include_path
    if not include_path.exists():
        # Ensure that the file exists
        return None
    return include_path


def recurssive_parser(path, visited=None):
    """Parse reccurssively all the configurations

    :param path: The path of the first config file
    :type path: pathlib.Path
    :param visited: The list of all dependencies which have been visited,
    defaults to None
    :type visited: list, optional
    :raises ProdexTemplateCircular: Raised if circular import is detected.
    :return: The data collected in all config files
    :rtype: dict
    """
    if path in visited:
        raise ProdexTemplateCircular("Circular Import detected in templates.")
    visited.append(path)

    # Parse the data
    with open(path, "r") as f:
        data = yaml.full_load(f)

    # Retrieve includes
    _includes = data.pop("includes", [])
    if _includes is None:
        _includes = []

    # Loop throught each includes
    for _include in _includes:

        include_path = get_include_as_absolute_path(
            file_name=path, include=_include
        )
        if not include_path:
            continue

        _data = recurssive_parser(path=include_path, visited=visited)

        for key in _data.keys():
            if key not in data:
                data[key] = _data[key]
                continue
            if isinstance(data[key], list):
                data[key].extend(_data[key])
            elif isinstance(data[key], dict):
                data[key].update(_data[key])
            else:
                data[key] = _data[key]

    # Put inlcudes inside the data
    data["includes"] = visited

    return data
