# -*- coding: utf-8 -*-
#
# - test_placeholders.py -
#
# Unit testing arround placeholders.
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
