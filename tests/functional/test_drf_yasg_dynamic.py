import pytest

from openapi_tester import validate_schema
from openapi_tester.exceptions import SpecificationError

good_test_data = [
    {
        'url': '/cars/correct/',
        'expected_response': [
            {'name': 'Saab', 'color': 'Yellow', 'height': 'Medium height', 'width': 'Very wide', 'length': '2 meters'},
            {'name': 'Volvo', 'color': 'Red', 'height': 'Medium height', 'width': 'Not wide', 'length': '2 meters'},
            {'name': 'Tesla', 'color': 'black', 'height': 'Medium height', 'width': 'Wide', 'length': '2 meters'},
        ],
    },
    {
        'url': '/trucks/correct/',
        'expected_response': [
            {'name': 'Saab', 'color': 'Yellow', 'height': 'Medium height', 'width': 'Very wide', 'length': '2 meters'},
            {'name': 'Volvo', 'color': 'Red', 'height': 'Medium height', 'width': 'Not wide', 'length': '2 meters'},
            {'name': 'Tesla', 'color': 'black', 'height': 'Medium height', 'width': 'Wide', 'length': '2 meters'},
        ],
    },
]
bad_test_data = [
    {
        'url': '/cars/incorrect/',
        'expected_response': [
            {'name': 'Saab', 'color': 'Yellow', 'height': 'Medium height'},
            {'name': 'Volvo', 'color': 'Red', 'width': 'Not very wide', 'length': '2 meters'},
            {'name': 'Tesla', 'height': 'Medium height', 'width': 'Medium width', 'length': '2 meters'},
        ],
    },
    {
        'url': '/trucks/incorrect/',
        'expected_response': [
            {'name': 'Saab', 'color': 'Yellow', 'height': 'Medium height'},
            {'name': 'Volvo', 'color': 'Red', 'width': 'Not very wide', 'length': '2 meters'},
            {'name': 'Tesla', 'height': 'Medium height', 'width': 'Medium width', 'length': '2 meters'},
        ],
    },
]


def test_endpoints_dynamic_schema(client) -> None:  # noqa: TYP001
    """
    Asserts that the validate_schema function validates correct schemas successfully.
    """
    for item in good_test_data:
        response = client.get('/api/v1' + item['url'])
        assert response.status_code == 200
        assert response.json() == item['expected_response']

        # Test Swagger documentation
        validate_schema(response, 'GET', item['url'])


def test_bad_endpoints_dynamic_schema(client) -> None:  # noqa: TYP001
    """
    Asserts that the validate_schema function validates incorrect schemas successfully.
    """
    for item in bad_test_data:
        response = client.get('/api/v1' + item['url'])
        assert response.status_code == 200
        assert response.json() == item['expected_response']

        # Test Swagger documentation
        with pytest.raises(SpecificationError, match='The following properties seem to be missing from your response body:'):
            validate_schema(response, 'GET', item['url'])
