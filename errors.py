class ProdexTemplateError(Exception):
    """Basic exception"""

    pass


class ProdexTemplateMissingPlaceholders(ProdexTemplateError):
    """Triyng to apply placaholders but one or more required are missing"""

    pass


class ProdexTemplateCircular(ProdexTemplateError):
    """Raise when a circular include is detected inside the configuration"""

    pass


### Placeholders errors


class ProdexTemplatePlaceholderValidation(ProdexTemplateError):
    """Raise when a value is not valid for the placeholder"""

    pass


class ProdexTemplatePlaceholderMultipleValues(ProdexTemplateError):
    """Raise when a placeholder received two different values"""

    pass


class ProdexTemplatePathSync(ProdexTemplateError):
    """Raise when the path and the definition are not synchronised. In most
    case, we can just say that the tested definition doesn't correspond
    to the tested path."""

    pass
