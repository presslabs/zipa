import pytest

from zipa import api_github_com as gh
from zipa import Resource
from mock import MagicMock

mock_Resource = MagicMock(Resource)


def test_resource_trait_names():
    assert mock_Resource.call_count == 0
    with pytest.raises(AttributeError):
        gh.trait_names
    assert mock_Resource.call_count == 0


def test_resource__getAttributeNames():
    assert mock_Resource.call_count == 0
    with pytest.raises(AttributeError):
        gh._getAttributeNames
    assert mock_Resource.call_count == 0
