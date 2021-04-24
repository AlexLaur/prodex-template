# -*- coding: utf-8 -*-
#
# - test_templates.py -
#
# Unit testing arround template system.
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

import os
import pathlib
import pytest

from templates import ProdexTemplate

SCRIPT_PATH = os.path.dirname(__file__)
CONFIG_FILENAME = os.path.join(SCRIPT_PATH, "fixtures", "template.yml")


@pytest.fixture
def config():
    return ProdexTemplate(path=CONFIG_FILENAME)


def test_get_template(config):
    """Get the corresponding template from the path"""
    path = "/prod/project/shot/work/maya/foo.v003.ma"
    expected = config.templates.get("maya_shot_work")
    assert config.template_from_path(path) == expected


def test_get_placeholders(config):
    """Get placeholders values from the path"""
    template = config.templates.get("houdini_asset_work_alembic_cache")
    path = "/prod/project/asset/work/houdini/cache/alembic/foo/render_node/v001/bar_foo_v001.abc"
    expected = {
        "name": "foo",
        "houdini_node": "render_node",
        "version": 1,
        "asset": "bar",
    }
    assert template.get_placeholders_values(path=path) == expected


def test_set_placeholder(config):
    """Set placeholders on template in order to generate a path"""
    template = config.templates.get("maya_asset_publish")
    placeholders = {"maya_extension": "mb", "version": 1, "name": "foo"}
    expected = pathlib.Path("/prod/project/asset/publish/maya/foo.v001.mb")
    assert (
        template.set_placeholders_values(placeholders=placeholders) == expected
    )


def test_validation_path(config):
    """Validation of a path for a template"""
    template = config.templates.get("photoshop_shot_snapshot")
    path = "/prod/project/shot/work/photoshop/snapshots/foo_bar.v003.0001.psd"
    expected = True
    assert template.validate(path=path) == expected
