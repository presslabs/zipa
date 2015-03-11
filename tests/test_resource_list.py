import httpretty
from zipa import api_test_com as t


def pretty_api():
    httpretty.register_uri(httpretty.GET, 'https://api.test.com/item',
                           status=200,
                           content_type='application/json',
                           body=u'[{"name": "a"}]')


class TestResourceIter(object):

    @httpretty.activate
    def test_returns_single_list(self):
        pretty_api()
        response = t.item()

        assert isinstance(response, list)
        assert response[0].name == "a"
