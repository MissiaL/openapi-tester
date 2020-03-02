import logging
from collections import OrderedDict
from json import dumps, loads

logger = logging.getLogger('openapi_tester')


def ordered_dict_to_dict(d: OrderedDict) -> dict:
    """
    Converts a nested OrderedDict to dict.
    """
    return loads(dumps(d))


def validate_path(schema_path: str, url_path: str):
    splitted_schema_path = schema_path.split('/')
    splitted_url_path = url_path.split('/')
    if len(splitted_schema_path) != len(splitted_url_path):
        return

    for index, part in enumerate(splitted_schema_path):
        if '{' in part:
            splitted_schema_path.remove(part)
            splitted_url_path.remove(splitted_url_path[index])

    if splitted_url_path == splitted_schema_path:
        return schema_path


def validate_paths(url: str, schema_paths: list):
    for path in schema_paths:
        result = validate_path(path, url)
        if result:
            return result
    raise KeyError(
        f'No path found for url `{url}`. Valid urls include {", ".join([key for key in schema_paths])}')


def fetch_generated_schema(url: str, method: str) -> dict:
    """
    Fetches dynamically generated schema.

    :param url: API endpoint URL, str
    :param method: HTTP method, str
    :return: dict
    """
    logger.debug('Fetching generated dynamic schema')
    from drf_yasg.openapi import Info
    from drf_yasg.generators import OpenAPISchemaGenerator

    base_schema = OpenAPISchemaGenerator(
        info=Info(title='', default_version='')).get_schema()
    schema = ordered_dict_to_dict(base_schema.as_odict())['paths']

    url = validate_paths(url, list(schema.keys()))
    schema = schema[url]

    try:
        schema = schema[method.lower()]['responses']
    except KeyError:
        raise KeyError(
            f'No schema found for method {method.upper()}. Available methods include '
            f'{", ".join([method.upper() for method in schema.keys() if method.upper() != "PARAMETERS"])}.'
        )
    try:
        if '$ref' in schema['200']['schema']:
            definition = schema['200']['schema']['$ref'].split('/')[-1]
            return ordered_dict_to_dict(base_schema.as_odict())['definitions'][definition]

        return schema['200']['schema']
    except KeyError:
        raise KeyError(
            f'No schema found for response code 200. Documented responses include '
            f'{", ".join([code for code in schema.keys() if code != "200"])}.'
            f'url: {url}'
        )