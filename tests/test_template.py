import os
import pathlib
import pytest

from templates import ProdexTemplate

SCRIPT_PATH = os.path.dirname(__file__)
CONFIG_FILENAME = os.path.join(SCRIPT_PATH, "fixtures", "template.yml")
CONFIG_OBJ = ProdexTemplate(path=CONFIG_FILENAME)


def test_get_template():
    """Get the corresponding template from the path"""
    path = "/prod/project/asset/publish/maya/foo/foo_bar_v001.ma"
    expected = CONFIG_OBJ.templates.get("maya_asset_publish")
    assert CONFIG_OBJ.template_from_path(path) == expected


def test_get_placeholders():
    """Get placeholders values from the path"""
    template = CONFIG_OBJ.templates.get("maya_asset_publish")
    path = "/prod/project/asset/publish/maya/foo/foo_bar_v001.ma"
    expected = {
        "maya_extension": "ma",
        "version": 1,
        "bar": "bar",
        "foo": "foo",
    }
    assert template.get_placeholders_values(path=path) == expected


def test_set_placeholder():
    """Set placeholders on template in order to generate a path"""
    template = CONFIG_OBJ.templates.get("maya_asset_publish")
    placeholders = {
        "maya_extension": "ma",
        "version": 1,
        "bar": "bar",
        "foo": "foo",
    }
    expected = pathlib.Path(
        "/prod/project/asset/publish/maya/foo/foo_bar_v001.ma"
    )
    assert (
        template.set_placeholders_values(placeholders=placeholders) == expected
    )


def test_validation_path():
    """Validation of a path for a template"""
    template = CONFIG_OBJ.templates.get("photoshop_file")
    path = "/prod/project/shot/work/test/photoshop/name.v001.psd"
    expected = True
    assert template.validate(path=path) == expected


def test_get_definitions():
    """Private method is tested here
    Try to get all possible definition for a template
    """
    expected = [
        "/prod/project/asset/publish/maya/{foo}_{baz}/{foo}_{bar}_v{version}.{maya_extension}",
        "/prod/project/asset/publish/maya/{foo}_{baz}/{foo}_v{version}.{maya_extension}",
        "/prod/project/asset/publish/maya/{foo}/{foo}_{bar}_v{version}.{maya_extension}",
        "/prod/project/asset/publish/maya/{foo}/{foo}_v{version}.{maya_extension}",
    ]
    template = CONFIG_OBJ.templates.get("maya_asset_publish")
    assert (
        template._definition_variations(definition=template._path) == expected
    )
