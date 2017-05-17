import pytest
import httpretty

from zipa import api_test_com as t


def pretty_api():
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.POST, 'http://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.PUT, 'http://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.PATCH, 'http://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.DELETE, 'http://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/b/c/d',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/s/resource',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')


@pytest.mark.httpretty
@pytest.mark.parametrize('method', ['__call__', 'post', 'put', 'delete', 'patch'])
def test_http_methods_over_simple_enpoint(method):
    pretty_api()
    t.config.secure = False
    t.config.headers = {
        'x-custom-header': 'custom-value'
    }

    assert getattr(t.a, method)().name == "a"
    assert httpretty.last_request().headers['x-custom-header'] == 'custom-value'


@pytest.mark.httpretty
def test_custom_url_as_resource():
    pretty_api()
    resource_url = "http://api.test.com/b/c/d"
    assert t.resource(resource_url)().name == "a"
    assert t.s.resource().name == "a"
