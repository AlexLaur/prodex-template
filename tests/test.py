import os

from pprint import pprint

from ..templates import ProdexTemplate

SCRIPT_PATH = os.path.dirname(__file__)

if __name__ == "__main__":
    config = ProdexTemplate(path=os.path.join(SCRIPT_PATH, "template.yml"))

    # '/prod/project/asset/publish/maya/{name}/pipi/{name}[_{test}]_v{version}.{maya_extension}'

    # name = alex
    # version = 001
    # maya_extention = ma
    # test = laurette
    # path = "/prod/project/asset/publish/maya/alex/alex_laurette_v001.ma"
    # path = "/prod/project/shot/work/test/photoshop/name.v001.psd"
    path = "/prod/project/asset/publish/maya/alex_flute/alex_laurette_v001.ma"

    # template = config.templates.get("photoshop_file")
    # print(template.validate(path))


    # pprint(config.templates)
    # pprint(config.strings)
    # pprint(config.placehodlers)

    template = config.templates.get("maya_asset_publish")

    # # print(template.validate(path=path))
    placeholders = template.get_placeholders_values(path=path)
    print(placeholders)

    # placeholders = {
    #     # "test": "hello",
    #     "name": "world",
    #     "version": 3,
    #     "maya_extension": "ma"
    # }

    test = template.set_placeholders_values(placeholders=placeholders)
    print(test)
    print(path)

    # templates = config.paths

    # template = templates.get("maya_asset_publish")

    # path = "/prod/project/asset/publish/maya/hello.v001.ma"
    # print(template.path)
    # print(template.validate(path=path))


    # config.template_from_path(path)