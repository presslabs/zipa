import time

import pytest
import httpretty
from mock import patch
from requests import HTTPError

from zipa import api_test_com as t
from .fixtures import pretty_api


@pytest.mark.httpretty
def test_retry_mechanism(pretty_api):
    start = time.time()

    t.config.secure = False
    t.config.backoff_max_attempts = 5

    t.retry()

    assert 0.5 < time.time() - start < 3
