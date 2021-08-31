import json

import httpretty
import pytest

from requests import HTTPError


@pytest.mark.httpretty()
@pytest.mark.parametrize('expected_response, status_code', [
    ({
        'customer': {
            'age': 55,
            'interests': ['photography', 'football'],
            'meta': {
                'A': '1234',
                'B': '4321',
            }
        }
    }, 200),
    ([{'a': 'b'}, {'c': 'd'}], 200),
    ({}, 200),
    ([], 200)
])
def test_default_response_handler_return_value(expected_response, status_code):
    from zipa import api_test_com as api
    api.config.secure = False

    httpretty.register_uri(httpretty.GET, 'http://api.test.com/item',
                           status=status_code,
                           content_type='application/json',
                           body=json.dumps(expected_response))

    assert api.item() == expected_response


@pytest.mark.httpretty()
@pytest.mark.parametrize('response_text, status_code, exception_str', [
    (u'{"detail": "Invalid input."}', 400, 'Errno 400 Client Error: Bad Request'),
    (u'{"detail": "I crashed."}', 500, 'Errno 500 Server Error: Internal Server Error')
])
def test_default_response_handler_error(response_text, status_code, exception_str):
    from zipa import api_test_com as api
    api.config.secure = False

    httpretty.register_uri(httpretty.GET, 'http://api.test.com/item',
                           status=status_code,
                           content_type='application/json',
                           body=response_text)

    with pytest.raises(HTTPError) as exception_info:
        api.item()

    http_error = exception_info.value
    assert exception_str in str(http_error)
    assert http_error.response.status_code == status_code
    assert http_error.response.text == response_text


@pytest.mark.httpretty()
def test_custom_response_handler_throw_exception():
    from zipa import api_testing_com as api

    def response_handler(response):
        if response.status_code == 500:
            raise ValueError('Not good')

    api.config.secure = False
    # NOTE: make sure to use different domains in order to prevent overwriting
    # response handler for other tests too.
    api.config.response_handler = response_handler

    httpretty.register_uri(httpretty.GET, 'http://api.testing.com/item',
                           status=500,
                           content_type='application/json',
                           body="hi")

    with pytest.raises(ValueError) as exception_info:
        api.item()

    assert str(exception_info.value) == 'Not good'


@pytest.mark.httpretty()
@pytest.mark.parametrize('return_value, expected_value', [
    (None, None),
    ({'default': [1, 2, 3]}, {'default': [1, 2, 3]}),
])
def test_custom_response_handler_return_value(return_value, expected_value):
    from zipa import api_t_com as api

    def response_handler(response):
        if response.status_code == 500:
            return return_value

    api.config.secure = False
    api.config.response_handler = response_handler

    httpretty.register_uri(httpretty.GET, 'http://api.t.com/item',
                           status=500,
                           content_type='application/json',
                           body="hi")

    assert api.item() == expected_value


def test_bad_json_response():
    from zipa import api_test_com as api
    api.config.secure = False

    httpretty.register_uri(httpretty.GET, 'http://api.test.com/bad_item',
                           status=200,
                           content_type='application/json',
                           body='{"bad json:" every where ')

    response = api.bad_item()
    # error masked by response handler.
    assert response == {}

    with pytest.raises(json.JSONDecodeError):
        list(api.bad_item[{"filter": "1"}])

