import pytest
import httpretty

from zipa import api_test_com as t
from .fixtures import pretty_api


@pytest.mark.httpretty
@pytest.mark.parametrize('method', ['__call__', 'post', 'put', 'delete', 'patch'])
def test_http_methods_over_simple_enpoint(method, pretty_api):
    t.config.secure = False
    t.config.headers = {
        'x-custom-header': 'custom-value'
    }

    assert getattr(t.a, method)().name == "a"
    assert httpretty.last_request().headers['x-custom-header'] == 'custom-value'


@pytest.mark.httpretty
def test_custom_url_as_resource(pretty_api):
    resource_url = "http://api.test.com/b/c/d"
    assert t.resource(resource_url)().name == "a"
    assert t.s.resource().name == "a"
