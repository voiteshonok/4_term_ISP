from lib.JsonParser import JsonParser
from lib.YamlParser import YamlParser

creators = {
    "json": JsonParser.JsonParser,
    "yaml": YamlParser.YamlParser
}


def get_serializer(format):
    creator = creators.get(format.lower())
    if not creator:
        raise ValueError(format)
    return creator()
