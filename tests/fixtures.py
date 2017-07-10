import pytest
import httpretty


@pytest.fixture
def pretty_api():
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/item/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/list',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item1": "name1"},{"item2": "name2"}]',
                           adding_headers={
                               'Link': '<http://api.test.com/list/2>; '
                                       'rel="next"',
                           })
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/list/2',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item3": "name3"},{"item4": "name4"}]',
                           adding_headers={
                               'Link': '<http://api.test.com/list/3>; '
                                       'rel="next"',
                           })
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/list/3',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item5": "name5"}]')

    httpretty.register_uri(httpretty.GET, 'http://api.test.com/list/first',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item1": "name1"},{"item2": "name2"}]',
                           adding_headers={
                               'Link': '<http://api.test.com/list/error>; '
                                       'rel="next"',
                           })
    httpretty.register_uri(httpretty.GET, 'http://api.test.com/list/error',
                           status=400,
                           content_type='application/json',
                           body=u'{"detail":"error"}')


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

    httpretty.register_uri(httpretty.GET, 'http://api.test.com/retry',
                           status=429, content_type='application/json')
