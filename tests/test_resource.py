import mock
import pytest

from zipa import api_github_com as gh
from zipa import Resource


@mock.patch('zipa.Resource')
def test_resource_trait_names(mock_Resource):
    assert mock_Resource.call_count == 0
    with pytest.raises(AttributeError):
        gh.trait_names
    assert mock_Resource.call_count == 0

@mock.patch('zipa.Resource')
def test_resource__getAttributeNames(mock_Resource):
    assert mock_Resource.call_count == 0
    with pytest.raises(AttributeError):
        gh._getAttributeNames
    assert mock_Resource.call_count == 0
