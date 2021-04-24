# -*- coding: utf-8 -*-
#
# - templates.py -
#
# Unit testtin arround templates utilities.
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

from utils import templates_utils


def test_parts_matching():
    """Test if path can match with one definition according to their parts"""
    definitions = [
        "/prod/project/shot/work/maya/snapshots/{name}/{shot}_{name}.v{version}.{timestamp}.{maya_extension}",
        "/prod/project/shot/work/maya/snapshots/{name}/{shot}_.v{version}.{timestamp}.{maya_extension}",
        "/prod/project/shot/work/maya/snapshots/{shot}_{name}.v{version}.{timestamp}.{maya_extension}",
        "/prod/project/shot/work/maya/snapshots/{shot}_.v{version}.{timestamp}.{maya_extension}",
    ]
    path = "/prod/project/shot/work/maya/snapshots/foo.v003.0002.ma"
    expected = True
    assert templates_utils.parts_matching(path, definitions) == expected


@pytest.mark.parametrize(
    "placeholder, expected",
    [("{foo}", True), ("{bar", False), ("baz", False), ("[{foo}]", False)],
)
def test_is_placeholder(placeholder, expected):
    """Test if the given placeholder is a valid placeholder"""
    assert templates_utils.is_placeholder(placeholder=placeholder) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            "/prod/project/shot/publish/photoshop/{name}.v{version}.psd",
            ["name", "version"],
        ),
        (
            "/prod/project/shot//work/maya/snapshots/{name}/{shot}_{name}.v{version}.{timestamp}.{maya_extension}",
            ["name", "shot", "name", "version", "timestamp", "maya_extension"],
        ),
    ],
)
def test_find_placeholder(path, expected):
    """Find all placeholders in the path"""
    assert templates_utils.find_placeholder(path=path) == expected


@pytest.mark.parametrize(
    "definition, expected",
    [
        (
            "/prod/project/shot/publish/photoshop/{name}.v{version}.psd",
            [
                "/prod/project/shot/publish/photoshop/",
                "name",
                ".v",
                "version",
                ".psd",
            ],
        ),
        (
            "/prod/project/shot//work/maya/snapshots/{name}/{shot}_{name}.v{version}.{timestamp}.{maya_extension}",
            [
                "/prod/project/shot//work/maya/snapshots/",
                "name",
                "/",
                "shot",
                "_",
                "name",
                ".v",
                "version",
                ".",
                "timestamp",
                ".",
                "maya_extension",
            ],
        ),
    ],
)
def test_find_static_parts(definition, expected):
    assert templates_utils.find_static_parts(definition=definition) == expected


@pytest.mark.parametrize(
    "definition, static_part, expected",
    [
        (
            "/prod/project/shot/review/{shot}_{name}_{nuke_output}_v{version}",
            "_v",
            (
                "/prod/project/shot/review/{shot}_{name}_{nuke_output}",
                "_v",
                "{version}",
            ),
        ),
        (
            "/prod/project/shot/review/{shot}_{name}_{nuke_output}",
            "_",
            ("/prod/project/shot/review/{shot}_{name}", "_", "{nuke_output}"),
        ),
    ],
)
def test_decompose_definition(definition, static_part, expected):
    """Decompose the definition with the static token"""
    assert (
        templates_utils.decompose_definition(definition, static_part)
        == expected
    )


def test_get_definitions():
    """Private method is tested here
    Try to get all possible definition for a template
    """
    expected = [
        "/prod/project/shot/work/maya/snapshots/{name}/{shot}_{name}.v{version}.{timestamp}.{maya_extension}",
        "/prod/project/shot/work/maya/snapshots/{name}/{shot}_.v{version}.{timestamp}.{maya_extension}",
        "/prod/project/shot/work/maya/snapshots/{shot}_{name}.v{version}.{timestamp}.{maya_extension}",
        "/prod/project/shot/work/maya/snapshots/{shot}_.v{version}.{timestamp}.{maya_extension}",
    ]
    definition = "/prod/project/shot/work/maya/snapshots[/{name}]/{shot}_[{name}].v{version}.{timestamp}.{maya_extension}"
    assert (
        templates_utils.find_definition_variations(definition=definition)
        == expected
    )
