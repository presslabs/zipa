import pytest
import httpretty
from requests.exceptions import HTTPError

from .fixtures import pretty_api
from zipa import api_test_com as t


@pytest.mark.httpretty
def test_iter_returns_single_object(pretty_api):
    t.config.secure = False

    for item in t.item['a']:
        assert item.name == 'a'


@pytest.mark.httpretty
def test_iter_completes(pretty_api):
    items = []
    t.config.secure = False

    for i in t.list:
        items.append(i)
    assert items == [{u'item1': u'name1'}, {u'item2': u'name2'},
                     {u'item3': u'name3'}, {u'item4': u'name4'},
                     {u'item5': u'name5'}]


@pytest.mark.httpretty
def test_iter_next_link_is_error(pretty_api):
    items = []
    t.config.secure = False

    with pytest.raises(HTTPError):
        for item in t.list.first:
            items.append(item)
