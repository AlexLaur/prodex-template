import os
from templates import ProdexTemplate

SCRIPT_PATH = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(SCRIPT_PATH, "tests", "fixtures", "template.yml")


if __name__ == "__main__":
    config = ProdexTemplate(path=CONFIG_PATH)

    path = "/prod/project/asset/publish/maya/alex/alex_laurette_v001.ma"
    # path = "/prod/project/shot/work/test/photoshop/name.v001.psd"
    print(path)

    # template = config.templates.get("maya_asset_publish")
    template = config.template_from_path(path=path)
    placeholders = template.get_placeholders_values(path=path)
    print(placeholders)

    new_path = template.set_placeholders_values(placeholders=placeholders)
    print(new_path)
