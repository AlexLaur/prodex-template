class ProdexTemplateError(Exception):
    """Basic exception"""

    pass


class ProdexTemplateMissingPlaceholders(ProdexTemplateError):
    """Triyng to apply placaholders but one or more required are missing"""

    pass


class ProdexTemplateCircular(ProdexTemplateError):
    """Raise when a circular include is detected inside the configuration"""
