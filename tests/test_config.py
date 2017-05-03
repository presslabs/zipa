import httpretty

from zipa import test_com as t


def test_config_zipa():
    t.config.host = 'random'
    t.config.prefix = 'prefix'
    t.config.append_slash = True
    t.config.secure = False
    t.config.headers = {
        'x-custom-header': 'custom-value'
    }

    assert t.config['host'] == 'random'
    assert t.config['prefix'] == 'prefix'
    assert t.config['append_slash']
    assert t.config['headers']['x-custom-header'] == 'custom-value'

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, 'http://randomprefix/a/', status=200,
                           content_type='application/json', body=u'{"name": "a"}')

    assert t.a().name == 'a'
    assert httpretty.last_request().headers['x-custom-header'] == 'custom-value'
