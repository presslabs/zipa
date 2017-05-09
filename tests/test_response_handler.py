import httpretty
import pytest

from requests import HTTPError


@httpretty.activate
def test_default_response_handler_client_error():
    from zipa import api_test_com as api
    api.config.secure = False

    response_text = u'{"detail": "Invalid input."}'
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/item',
                           status=400,
                           content_type='application/json',
                           body=response_text)

    with pytest.raises(HTTPError) as exception_info:
        api.item()

    http_error = exception_info.value
    assert 'Errno 400 Client Error: Bad Request' in str(http_error)
    assert http_error.response.status_code == 400
    assert http_error.response.text == response_text


@httpretty.activate
def test_default_response_handler_server_error():
    from zipa import api_test_com as api
    api.config.secure = False

    response_text = u'{"detail": "I crashed."}'
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/item',
                           status=500,
                           content_type='application/json',
                           body=response_text)

    with pytest.raises(HTTPError) as exception_info:
        api.item()

    http_error = exception_info.value
    assert 'Errno 500 Server Error: Internal Server Error' in str(http_error)
    assert http_error.response.status_code == 500
    assert http_error.response.text == response_text


@httpretty.activate
def test_custom_response_handler_throw_exception():
    from zipa import api_test_com as api

    def response_handler(response):
        if response.status_code == 500:
            raise ValueError('Not good')

    api.config.secure = False
    api.config.response_handler = response_handler

    httpretty.register_uri(httpretty.GET, 'http://api.test.com/item',
                           status=500,
                           content_type='application/json',
                           body="hi")

    with pytest.raises(ValueError) as exception_info:
        api.item()

    assert str(exception_info.value) == 'Not good'


@pytest.mark.httpretty()
@pytest.mark.parametrize('return_value, expected_value', [
    (None, {}),
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
