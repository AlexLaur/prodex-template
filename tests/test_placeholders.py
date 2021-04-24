import pytest

from placeholders import IntegerPlaceholder, StringPlaceholder


@pytest.fixture
def string_placeholder():
    return StringPlaceholder(name="foo", type="str")


@pytest.fixture
def string_placeholder_choices():
    return StringPlaceholder(name="foo", type="str", choices=["bar", "baz"])


@pytest.fixture
def integer_placeholder():
    return IntegerPlaceholder(name="bar", type="int")


@pytest.fixture
def integer_placeholder_choices():
    return IntegerPlaceholder(name="bar", type="int", choices=[1, 2])


@pytest.fixture
def integer_placeholder_format_spec():
    return IntegerPlaceholder(name="bar", type="int", format_spec=3)


@pytest.mark.parametrize(
    "string, expected", [("foo", True), ("001", True), (1, True)]
)
def test_simple_string_validation(string_placeholder, string, expected):
    """Test the validation with a simple placeholder"""
    assert string_placeholder.validate(string) == expected


@pytest.mark.parametrize(
    "string, expected", [("foo", False), ("bar", True), ("baz", True)]
)
def test_choice_string_validation(
    string_placeholder_choices, string, expected
):
    """Test the validation with a placeholder which have fixed choices"""
    assert string_placeholder_choices.validate(string) == expected


@pytest.mark.parametrize(
    "integer, expected", [("foo", False), ("001", True), (1, True)]
)
def test_simple_integer_validation(integer_placeholder, integer, expected):
    """Test the validation with a simple placeholder"""
    assert integer_placeholder.validate(integer) == expected


@pytest.mark.parametrize(
    "integer, expected", [("0", False), (1, True), ("002", True), (3, False)]
)
def test_choice_integer_validation(
    integer_placeholder_choices, integer, expected
):
    """Test the validation with a placeholder which have fixed choices"""
    assert integer_placeholder_choices.validate(integer) == expected


# @pytest.mark.parametrize(
#     "integer, expected", [(1, False), ("001", True), ("0001", False)]
# )
# def test_format_spec_integer_validation(integer_placeholder_format_spec, integer, expected):
#     """Test the validation with the format spec"""
#     assert integer_placeholder_format_spec.validate(integer) == expected
