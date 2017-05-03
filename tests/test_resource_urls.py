class TestResourceUrls(object):
    def test_naked_domain(self):
        from zipa import api_test_net as t
        assert t._get_url() == 'https://api.test.net/'

    def test_with_version_in_url(self):
        from zipa import api_test_net__v1 as t
        assert t._get_url() == 'https://api.test.net/v1/'

    def test_with_deep_path(self):
        from zipa import test_net__api_v1 as t
        assert t._get_url() == 'https://test.net/api/v1/'

    def test_simple_method_with_naked_domain(self):
        from zipa import api_test_net as t
        assert t.res._get_url() == 'https://api.test.net/res'

    def test_simple_method_with_version_in_url(self):
        from zipa import api_test_net__v1 as t
        assert t.res._get_url() == 'https://api.test.net/v1/res'

    def test_simple_method_with_deep_path(self):
        from zipa import test_net__api_v1 as t
        assert t.res._get_url() == 'https://test.net/api/v1/res'

    def test_new_resource_url(self):
        from zipa import test_net as t

        new_url = "https://test.net/api/v1"
        t.resource("%s/d" % new_url)._get_url() == "%s/d" % new_url
