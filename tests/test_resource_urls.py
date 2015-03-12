class TestResourceUrls(object):
    def test_naked_domain(self):
        from zipa import api_test_com as t
        assert t._get_url() == 'https://api.test.com/'

    def test_with_version_in_url(self):
        from zipa import api_test_com__v1 as t
        assert t._get_url() == 'https://api.test.com/v1/'

    def test_with_deep_path(self):
        from zipa import test_com__api_v1 as t
        assert t._get_url() == 'https://test.com/api/v1/'

    def test_simple_method_with_naked_domain(self):
        from zipa import api_test_com as t
        assert t.res._get_url() == 'https://api.test.com/res'

    def test_simple_method_with_version_in_url(self):
        from zipa import api_test_com__v1 as t
        assert t.res._get_url() == 'https://api.test.com/v1/res'

    def test_simple_method_with_deep_path(self):
        from zipa import test_com__api_v1 as t
        assert t.res._get_url() == 'https://test.com/api/v1/res'

    def test_new_resource_url(self):
        from zipa import test_com as t

        new_url = "https://test.com/api/v1"
        t.resource("%s/d" % new_url)._get_url() == "%s/d" % new_url
