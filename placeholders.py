
class Placeholder(object):
    def __init__(self, name, type, *args, **kwargs):

        self.name = name
        self.choices = kwargs.get("choices", [])
        self.length = kwargs.get("length", None)
        self.default = kwargs.get("default", None)

    def __repr__(self):
        return "<%s %s>" % (
            __class__.__name__,
            self.name,
        )

    def __str__(self):
        return "%s %s" % (__class__.__name__, self.name)

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
    def __init__(self, name, *args, **kwargs):
        super(IntegerPlaceholder, self).__init__(name=name, *args, **kwargs)

        self.format_spec = kwargs.get("format_spec", "%01d")
        # self.length = kwargs.get("length", 1)

    def validate(self, value):
        """Test if a value is valid for this placeholder.

        :param value: The value to test.
        :return: True if the value is valid, False if not.
        :rtype: bool
        """
        if isinstance(value, int):
            return True
        if not value.isdigit():
            return False
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
    def __init__(self, name, *args, **kwargs):
        super(StringPlaceholder, self).__init__(name=name, *args, **kwargs)

    def validate(self, value):
        """Test if a value is valid for this placeholder.

        :param value: The value to test.
        :return: True if the value is valid, False if not.
        :rtype: bool
        """
        return super(StringPlaceholder, self).validate(value=value)
