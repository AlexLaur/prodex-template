# -*- coding: utf-8 -*-
#
# - placeholders.py -
#
# All mecanisms arround placeholders.
#
# Copyright (c) 2021 Laurette Alexandre
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class Placeholder(object):
    """Basic class for Placeholders. A placeholder is represented by an
    ambrassed word in a path. e.g: {foo}"""

    def __init__(self, name, type, *args, **kwargs):

        self.name = name
        self.choices = kwargs.get("choices", [])
        self.length = kwargs.get("length", None)
        self.default = kwargs.get("default", None)

    def __repr__(self):
        return "<%s %s>" % (
            self.__class__.__name__,
            self.name,
        )

    def __str__(self):
        return "%s %s" % (self.__class__.__name__, self.name)

    def validate(self, value):
        """
        Test if a value is valid for this placeholder::
            >>> StringPlaceholder.validate('foo')
            >>> True
            >>> IntegerPlaceholder.validate(2)
            >>> True
            >>> IntegerPlaceholder.validate('foo')
            >>> False
        :param value: Value to test
        :return: True if the value is valid, False instead.
        :rtype: Bool
        """
        if self.choices:
            if value not in self.choices:
                return False
        if self.length:
            if len(str(value)) != self.length:
                return False
        return True

    def conform_value(self, value):
        """Conform the value for this placeholder
        >>> IntegerPlaceholder.conform_value(3)
        >>> "003"

        :param value: The value to conform
        :return: The conformed value
        """
        return value

    def sanitize_value(self, value):
        """Sanitize the value for this placeholder

        >>> IntegerPlaceholder.sanitize_value("003")
        >>> 3

        :param value: The value to sanitize
        :return: The sanitize value
        """
        return value


class IntegerPlaceholder(Placeholder):
    """IntegerPlaceholder represents a Placeholder
    which will contain an Integer.
    """

    def __init__(self, name, *args, **kwargs):
        super(IntegerPlaceholder, self).__init__(name=name, *args, **kwargs)

        self.format_spec = kwargs.get("format_spec", 1)

    def validate(self, value):
        """Test if a value is valid for this placeholder.

        :param value: The value to test.
        :return: True if the value is valid, False if not.
        :rtype: bool
        """
        if isinstance(value, str) and not value.isdigit():
            return False
        if not isinstance(self.sanitize_value(value), int):
            return False
        value = self.sanitize_value(value)
        return super(IntegerPlaceholder, self).validate(value=value)

    def conform_value(self, value):
        """Conform the value for this placeholder

        :param value: The value to conform
        :return: The conformed value
        """
        value = str(value).zfill(self.format_spec)
        return value

    def sanitize_value(self, value):
        """Sanitize the value for this placeholder

        :param value: The value to sanitize
        :return: The sanitize value
        """
        return int(value)


class StringPlaceholder(Placeholder):
    """StringPlaceholder represents a placeholder which will contain a string."""

    def __init__(self, name, *args, **kwargs):
        super(StringPlaceholder, self).__init__(name=name, *args, **kwargs)

    def validate(self, value):
        """Test if a value is valid for this placeholder.

        :param value: The value to test.
        :return: True if the value is valid, False if not.
        :rtype: bool
        """
        return super(StringPlaceholder, self).validate(value=value)


PLACEHOLDERS_MAPPING = {"str": StringPlaceholder, "int": IntegerPlaceholder}
