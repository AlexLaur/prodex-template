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
