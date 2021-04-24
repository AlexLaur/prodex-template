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


def is_placeholder(placeholder):
    """Test if the placeholder is a correct placeholder.
    To be a correct placeholder, the placeholder needs to be embrasse
    like this : {placeholder}

    >>> is_placeholder("{foo}")
    >>> True
    >>> is_placeholder("{bar")
    >>> False
    >>> is_placeholder("baz")
    >>> False

    :param placeholder: The placeholder to test
    :type placeholder: str
    :return: True if it is ok, False if not
    :rtype: bool
    """
    if re.match(r"{(\w+)}", placeholder):
        return True
    return False


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


def find_static_parts(definition):
    """Find static parts in the definition. Static parts are some elements
    between placeholders.

    :param definition: The definition to analyse
    :type definition: str
    :return: All static parts
    :rtype: list
    """
    tokens = re.split(r"{(\w+)}", definition)
    # Remove empty strings
    return [x for x in tokens if x]


def find_definition_variations(definition):
    """Finds all possible paths for the given definition (from the template)

    "{foo}"               ==> ['{foo}']
    "{foo}_{bar}"         ==> ['{foo}_{bar}']
    "{foo}[_{bar}]"       ==> ['{foo}', '{foo}_{bar}']
    "{foo}_[{bar}_{baz}]" ==> ['{foo}_', '{foo}_{bar}_{baz}']
    """
    # split definition by optional sections
    static_parts = re.split(r"(\[[^]]*\])", str(definition))

    # seed with empty string
    definitions = [""]
    for static_part in static_parts:
        temp_definitions = []
        # regex return some blank strings, skip them
        if static_part == "":
            continue
        if static_part.startswith("["):
            # check that optional contains a key
            if not re.search(r"{(\w+)}", static_part):
                raise Exception(
                    'Optional sections must include a key definition. Token: "%s" Template: %s'
                    % (static_part, self)
                )

            # Add definitions skipping this optional value
            temp_definitions = definitions[:]
            # strip brackets from static_part
            static_part = re.sub(r"[\[\]]", "", static_part)

        # check non-optional contains no dangleing brackets
        if re.search(r"[\[\]]", static_part):
            raise Exception(
                "Square brackets are not allowed outside of optional section definitions."
            )

        # make defintions with static_part appended
        for definition in definitions:
            temp_definitions.append(str(definition) + static_part)

        definitions = temp_definitions

    # Sort the list DESC
    definitions.sort(key=lambda x: len(x), reverse=True)

    return definitions


def decompose_definition(definition, static_part):
    """Decompose a definition in order to have a static part followed by a
    placeholder

    >>> definition = "/prod/project/shot/review/{shot}_{name}_{nuke_output}_v{version}"
    >>> static_part = "_v"
    >>> decompose_definition(definition, static_part)
    >>> ('/prod/project/shot/review/{shot}_{name}_{nuke_output}', '_v', '{version}')

    >>> definition = "/prod/project/shot/review/{shot}_{name}_{nuke_output}"
    >>> static_part = "_"
    >>> decompose_definition(definition, static_part)
    >>> ('/prod/project/shot/review/{shot}_{name}', '_', '{nuke_output}')

    :param definition: The definition to decompose
    :type definition: str
    :param static_part: The static part (element between two placeholders)
    :type static_part: str
    :return: The decomposed definition
    :rtype: tuple
    """
    decompose = definition.rpartition(static_part)
    if not decompose[-1]:
        # In some case when the definition doesn't end by a placeholders
        return decompose
    if is_placeholder(placeholder=decompose[-1]):
        # It is a fully placeholder
        return decompose
    # At this point, it is a partial placeholder. We need to find where is the
    # right static_part
    count = 1
    placeholder = definition[-count]
    while not is_placeholder(placeholder):
        placeholder = definition[-count:]
        count += 1
    base = definition[0 : len(definition) - count]
    return (base, static_part, placeholder)


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


def sanitize_link(link):
    return link.strip().partition(".")[0]
