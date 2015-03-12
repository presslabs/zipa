import httpretty

from zipa import api_test_com as t


def pretty_api():
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.POST, 'https://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.PUT, 'https://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.PATCH, 'https://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.DELETE, 'https://api.test.com/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/b/c/d',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/s/resource',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')



class TestResourceIter(object):

    @httpretty.activate
    def test_http_methods_over_simple_enpoint(self):
        pretty_api()

        assert t.a().name == "a"
        assert t.a.post().name == "a"
        assert t.a.put().name == "a"
        assert t.a.delete().name == "a"
        assert t.a.patch().name == "a"

        resource_url = "https://api.test.com/b/c/d"
        assert t.resource(resource_url)().name == "a"

        assert t.s.resource().name == "a"
