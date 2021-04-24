import re
import yaml
import pathlib

from utils import paths_utils, templates_utils
from placeholders import (
    StringPlaceholder,
    IntegerPlaceholder,
    PLACEHOLDERS_MAPPING,
)
import errors

from pprint import pprint


class ProdexTemplate(object):
    def __init__(self, path):
        super(ProdexTemplate, self).__init__()

        # Constants
        self.template_path = pathlib.Path(path)
        self._paths = {}
        self._root_paths = {}
        self._content = None

        self._placeholders = {}
        self._templates = {}
        self._strings = {}

        # Init vars
        self._content = paths_utils.recurssive_parser(
            path=self.template_path, visited=[]
        )
        self._paths, self._root_paths = templates_utils.paths_categorization(
            paths=self._content.get("paths", {})
        )
        self._strings = self._content.get("strings", {})

        #
        self._parse_placeholders()
        self._parse_templates()

    @property
    def templates(self):
        """Return a copy of all templates

        :return: Dictionnary of all templates (key: template name)
        (value: template object)
        :rtype: dict
        """
        return self._templates.copy()

    @property
    def placeholders(self):
        """Return a copy of all placeholders

        :return: Dictionnary of all placeholders (key: placeholder name)
        (value: placeholder object)
        :rtype: dict
        """
        return self._placeholders.copy()

    @property
    def strings(self):
        """Return a copy of all strings

        :return: Dictionnary of all strings (key: string name)
        (value: string object)
        :rtype: dict
        """
        return self._strings.copy()

    def _parse_templates(self):
        """Parse all templates found in the configuration"""
        for template_name, template_path in self._paths.items():

            path = template_path.get("definition")
            path = pathlib.Path(path)

            parts = list(path.parts)

            for index, part in enumerate(path.parts):
                if index == 0 and part.startswith("@"):
                    static_part = templates_utils.sanitize_link(link=part)
                    found = self._root_paths.get(static_part[1::], None)
                    if not found:
                        raise errors.ProdexTemplateError(
                            "No root path found for %s" % part
                        )
                    parts[index] = found

                elif part.startswith("@"):
                    static_part = templates_utils.sanitize_link(link=part)
                    found = self._strings.get(static_part[1::], None)
                    if not found:
                        raise errors.ProdexTemplateError(
                            "No string path found for %s" % part
                        )
                    parts[index] = found

            new_path = pathlib.Path(*parts)
            template_path["definition"] = new_path

            placeholders_found = templates_utils.find_placeholder(
                path=str(new_path)
            )
            placeholders = {
                x: v
                for x, v in self._placeholders.items()
                if x in placeholders_found
            }

            template = Template(
                definition=new_path,
                name=template_name,
                placeholders=placeholders,
            )
            self._templates[template_name] = template

    def _parse_placeholders(self):
        """Parses placeholders of the configuration"""
        placeholders = self._content.get("placeholders")
        for placehodler_name, attributes in placeholders.items():
            class_object = PLACEHOLDERS_MAPPING.get(attributes.get("type"))
            placeholder = class_object(name=placehodler_name, **attributes)
            self._placeholders[placehodler_name] = placeholder

    def templates_from_path(self, path):
        """Finds templates that matches the given path

        :param path: The path to match against a template
        :type path: str
        :return: List of :class:`Template` or [] if no match could be found.
        :rtype: list
        """
        found = []
        for template_name, template in self._templates.items():
            if not template.validate(path):
                continue
            found.append(template)
        return found

    def template_from_path(self, path):
        """Finds a template that matches the given path

        :param path: The path to match against a template
        :type path: str
        :return: :class:`Template` or None if no match could be found.
        :rtype: :class:`Template`
        """
        matched_templates = self.templates_from_path(path)

        if not matched_templates:
            return None
        elif len(matched_templates) == 1:
            return matched_templates[0]
        else:
            # Multiple templates
            raise errors.ProdexTemplateError(
                "Multiple templates found: {}".format(matched_templates)
            )


class String(object):
    def __init__(self):
        pass


class Template(object):
    def __init__(self, definition, name, placeholders):

        self._path = definition
        self._name = name
        self._placeholders = placeholders

        self._all_definitions = templates_utils.find_definition_variations(
            self._path
        )

    def __repr__(self):
        return self._get_repr()

    def __str__(self):
        return self._get_repr()

    def _get_repr(self):
        return "<%s %s: %s>" % (
            self.__class__.__name__,
            self._name,
            self._path,
        )

    @property
    def path(self):
        """Return the default path (from the config file) of this template

        :return: The path of this template
        :rtype: str
        """
        return self._path

    @property
    def placeholders(self):
        """Return a copy of all placeholders found for this template

        :return: Dictionnary of all placeholders. Keys are the name of the
        placeholder. Values are the corresponding Placeholder object
        :rtype: dict
        """
        return self._placeholders.copy()

    @property
    def definitions(self):
        """Return a copy of all definitions found for this template

        :return: List of all definitions
        :rtype: list
        """
        return self._all_definitions.copy()

    def validate(self, path):
        """Validate or not the given path.

        :param path: The path to validate
        :type path: str
        :return: True if the path is correct for this template, False if not
        :rtype: bool
        """
        # 1. Check if the number of parts in the given path correspond
        # to the number of parts for an existing definition for this template
        if not templates_utils.parts_matching(
            path=path, definitions=self.definitions
        ):
            return False

        # 2. Try to resolve placeholders. If we found something, the path is
        # correct, if not, the path doesn't fit the template.
        resolved_placeholders = self.get_placeholders_values(
            path=path, discreet=True
        )
        if not resolved_placeholders:
            return False

        # 3. Be sure that we can generate the same path
        # with the resolved placeholders (ensure the paths are equals)
        match = False
        self._conform_input_placeholders(placeholders=resolved_placeholders)
        for definition in self.definitions:
            _path = self._set_placeholders_values(
                definition=definition, placeholders=resolved_placeholders
            )
            if str(_path) == path:
                match = True
        return match

    def get_placeholders_values(self, path, **kwargs):
        """Gets the placeholders values from the given path.

        Example::
        Considering the following template:
        maya_asset_work:
            definition: '/prod/poject/{project}/{name}_v{version}.{maya_extension}'
            >>> path = '/prod/project/foo/bar_v001.ma'
            >>> get_placeholders_values(path=path)
            >>> {"project": "foo", "name": "bar", "version": 1, "maya_extension": "ma"}

        :param path: The input path
        :type path: str
        :param discreet: (kwargs) Raise errors, optional
        :type discreet: bool
        :returns: Values found Values in the path based on placeholders in template
        :rtype: dict
        """
        discreet = kwargs.get("discreet", False)  # False: raise errors
        error = None
        # loop through all definitions
        for definition in self.definitions:
            resolved = {}  # All resolved placeholders
            _definition = definition
            _path = path
            static_parts = templates_utils.find_static_parts(
                definition=definition
            )
            static_parts.reverse()

            if static_parts[0] not in self.placeholders:
                static_part = static_parts[0]
                # The first static_part is not a placeholder. So, transform the path
                # and the definition in order to start by a placeholder
                _path = path.rpartition(static_part)[0]
                _definition = templates_utils.decompose_definition(
                    definition=definition, static_part=static_part
                )[0]
                # Remove the first static_part because we want to start
                # by a placeholder
                static_parts = static_parts[1::]

            static_parts = [
                x for x in static_parts if x not in self.placeholders
            ]
            for static_part in static_parts:
                path_decompose = _path.rpartition(static_part)
                definition_decompose = templates_utils.decompose_definition(
                    definition=_definition, static_part=static_part
                )

                key = definition_decompose[-1]
                value = path_decompose[-1]

                placeholder_obj = self.placeholders.get(key.strip("{}"))
                if not placeholder_obj.validate(value):
                    # The value is not conform for the given placeholder
                    error = errors.ProdexTemplatePlaceholderValidation(
                        "The value {0} is not conform for the placeholder {1}".format(
                            value, placeholder_obj.name
                        )
                    )
                    break

                # All values are empty
                if len(set(path_decompose)) == 1:
                    # path and static_part are not synchronized,
                    # so it is not the path what we are looking for
                    error = errors.ProdexTemplatePathSync(
                        "Path and the static_part aren't synchronised anymore"
                    )
                    break

                if placeholder_obj.name in resolved:
                    # already analysed, check that the value is the same
                    _value = resolved.get(placeholder_obj.name)
                    value = placeholder_obj.sanitize_value(value)
                    if value != _value:
                        error = errors.ProdexTemplatePlaceholderMultipleValues(
                            "Got two differents values for the {0} [{1}, {2}]".format(
                                placeholder_obj.name, _value, value
                            )
                        )
                        break
                else:
                    error = None
                    resolved[
                        placeholder_obj.name
                    ] = placeholder_obj.sanitize_value(value)

                _path = path_decompose[0]
                _definition = definition_decompose[0]

            placeholders = list(
                set(templates_utils.find_placeholder(definition))
            )
            if len(placeholders) == len(resolved) and not error:
                # find all possible values.
                return resolved
            else:
                resolved = {}
        if not discreet:
            raise error
        return resolved

    def set_placeholders_values(self, placeholders):
        """Apply given placeholders to the current template in order
        to generate a path.

        :param placeholders: Placeholders to apply
        :type placeholders: dict
        :raises ValueError: Raised if a placeholder is not valid
        :raises errors.ProdexTemplateMissingPlaceholders: If a required
        placeholder is missing
        :return: The generated path
        :rtype: pathlib.Path
        """
        # Check each placeholders
        if not self._check_input_placeholders(placeholders=placeholders):
            raise errors.ProdexTemplateError()

        # Conform each placeholders
        self._conform_input_placeholders(placeholders=placeholders)

        # Apply placeholders
        for definition in self.definitions:
            path = self._set_placeholders_values(
                definition=definition, placeholders=placeholders
            )
            if path:
                # Path found ! return it.
                return pathlib.Path(path)
        return None

    def _set_placeholders_values(self, definition, placeholders):
        """Apply placeholders on a definition

        :param definition: The definition on which apply placeholders
        :type definition: str
        :param placeholders: Dictionnary of key: value placeholders
        :type placeholders: dict
        :return: The generated path
        :rtype: str
        """
        # https://stackoverflow.com/questions/17215400/format-string-unused-named-arguments
        path = definition.format_map(
            templates_utils.SafeDict(**placeholders)
        )  # Py3
        unresolved_placeholders = templates_utils.find_placeholder(path)
        if unresolved_placeholders:
            # We have unresolved placeholder
            # raise errors.ProdexTemplateMissingPlaceholders(
            #     "Required placeholders missing : %s" % unresolved_placeholders
            #     )
            return None
        return path

    def _check_input_placeholders(self, placeholders):
        """Check given placeholders with detected placeholders in the current
        template.

        :param placeholders: Placeholders to apply.
        :type placeholders: dict
        :return: True if the check is done, False instead
        :rtype: bool
        """
        for key, value in placeholders.items():
            if key not in self.placeholders:
                continue
            if not self.placeholders.get(key).validate(value):
                return False
        return True

    def _conform_input_placeholders(self, placeholders):
        """Conform the given placeholder. If a placeholder is not given, but
        if it has a default value, the default value will be added to the
        placeholders dict in order to resolve the path.

        :param placeholders: All given placeholders
        :type placeholders: dict
        :return: The conformed placeholders
        :rtype: dict
        """
        evaluated = []
        for key, value in placeholders.items():
            evaluated.append(key)
            if key not in self.placeholders:
                continue
            placeholders[key] = self.placeholders.get(key).conform_value(value)

        missing_placeholders = [
            x for x in self.placeholders if x not in evaluated
        ]

        # Check missing placeholder for default values
        for key in missing_placeholders:
            if not self.placeholders.get(key).default:
                continue
            placeholders[key] = self.placeholders.get(key).default
        return placeholders
