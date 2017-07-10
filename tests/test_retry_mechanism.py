import time
import random

import pytest
import httpretty
from mock import MagicMock, call
from requests import HTTPError

from zipa import api_test_retry as t
from .fixtures import pretty_api


@pytest.mark.httpretty
def test_retry_mechanism_no_sleep(pretty_api, monkeypatch):
    mocked_sleep = MagicMock()
    mocked_random = MagicMock(return_value=1)

    t.config.secure = False
    t.config.backoff_max_attempts = 5

    monkeypatch.setattr(time, 'sleep', mocked_sleep)
    monkeypatch.setattr(random, 'uniform', mocked_random)

    with pytest.raises(HTTPError):
        t.retry()

    mocked_random.assert_has_calls([
        call(0, 0.1 * 2 ** 0),
        call(0, 0.1 * 2 ** 1),
        call(0, 0.1 * 2 ** 2),
        call(0, 0.1 * 2 ** 3),
        call(0, 0.1 * 2 ** 4),
    ])

    mocked_sleep.assert_has_calls([
        call(1),
        call(1),
        call(1),
        call(1),
        call(1),
    ])
