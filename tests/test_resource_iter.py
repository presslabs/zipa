import httpretty
import pytest

from requests.exceptions import HTTPError
from zipa import api_test_com as t


def pretty_api():
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/item/a',
                           status=200,
                           content_type='application/json',
                           body=u'{"name": "a"}')

    httpretty.register_uri(httpretty.GET, 'https://api.test.com/list',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item1": "name1"},{"item2": "name2"}]',
                           adding_headers={
                               'Link': '<https://api.test.com/list/2>; '
                                       'rel="next"',
                           })
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/list/2',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item3": "name3"},{"item4": "name4"}]',
                           adding_headers={
                               'Link': '<https://api.test.com/list/3>; '
                                       'rel="next"',
                           })
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/list/3',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item5": "name5"}]')

    httpretty.register_uri(httpretty.GET, 'https://api.test.com/list/first',
                           status=200,
                           content_type='application/json',
                           body=u'[{"item1": "name1"},{"item2": "name2"}]',
                           adding_headers={
                               'Link': '<https://api.test.com/list/error>; '
                                       'rel="next"',
                           })
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/list/error',
                           status=400,
                           content_type='application/json',
                           body=u'{"detail":"error"}')


class TestResourceIter:

    @httpretty.activate
    def test_iter_returns_single_object(self):
        pretty_api()
        for i in t.item['a']:
            assert i.name == 'a'

    @httpretty.activate
    def test_iter_completes(self):
        pretty_api()
        items = []
        for i in t.list:
            items.append(i)
        assert items == [{u'item1': u'name1'}, {u'item2': u'name2'},
                         {u'item3': u'name3'}, {u'item4': u'name4'},
                         {u'item5': u'name5'}]

    @httpretty.activate
    def test_iter_next_link_is_error(self):
        pretty_api()
        items = []
        with pytest.raises(HTTPError):
            for i in t.list.first:
                items.append(i)
