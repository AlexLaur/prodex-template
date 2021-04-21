[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# prodex-template

Template system inspired by the template system developped by `Autodesk Shotgun` in their toolkit (`sgtk`)

- The system use the same config file style as `sgtk`.
- For placeholders, only Integer and String exists.
- This only work for linux and on Python3 for this moment.
---
### Examples

Get the template for a path
```python
>>> path = "/prod/project/asset/publish/maya/foo/foo_bar_v001.ma"
>>> template = templates.template_from_path(path=path)
>>> <Template maya_asset_publish: /prod/project/asset/publish/maya/{foo}[_{baz}]/{foo}[_{bar}]_v{version}.{maya_extension}>
```

Get placeholders values
```python
>>> path = "/prod/project/asset/publish/maya/foo/foo_bar_v001.ma"
>>> template = templates.get("maya_asset_publish")
>>> template.get_placeholders_values(path=path)
>>> {"maya_extension": "ma", "version": 1, "bar": "bar", "foo": "foo"}
```

Generate a path from placeholders
```python
>>> placeholders = {"maya_extension": "ma", "version": 1, "bar": "bar", "foo": "foo"}
>>> template = templates.get("maya_asset_publish")
>>> template.set_placeholders_values(placeholders=placeholders)
>>> "/prod/project/asset/publish/maya/foo/foo_bar_v001.ma"
```
---
### Tests
It use `pytest` for unit testing.
```bash
$ pytest
```
---
### Todo
- Python2.7 compatibility (for existing pipelines).
- More placeholders type like Sequence, Datetime.
- More efficiency.