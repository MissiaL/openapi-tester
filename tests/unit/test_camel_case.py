import pytest

from openapi_tester.case_checks import is_camel_case
from openapi_tester.exceptions import SpecificationError

camel_case_test_data = [
    {'incorrect': 'snake_case', 'correct': 'snakeCase'},
    {'incorrect': 'PascalCase', 'correct': 'pascalCase'},
    {'incorrect': 'kebab-case', 'correct': 'kebabCase'},
    {'incorrect': 'l ower', 'correct': 'lower'},
    {'incorrect': 'UPPER', 'correct': 'uPPER'},
]


def test_camel_cased_words():
    """
    Verifies that our camel case verification function actually works as expected.
    """
    for item in camel_case_test_data:
        is_camel_case(item['correct'])
        with pytest.raises(SpecificationError):
            is_camel_case(item['incorrect'])


def test_less_than_two_chars():
    """
    When the length of an input is less than 2, our regex logic breaks down,
    :return:
    """
    is_camel_case('')
    with pytest.raises(SpecificationError):
        is_camel_case(' ')
        is_camel_case('-')
        is_camel_case('_')
        is_camel_case(None)
        is_camel_case('%')
        is_camel_case('R')
    is_camel_case('s')
