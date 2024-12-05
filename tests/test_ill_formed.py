from __future__ import annotations

import datetime
import pathlib
import typing

import pytest

import feedparser

from .helpers import (
    everything_is_unicode,
    get_file_contents,
    get_http_test_data,
    get_test_data,
)

tests: list[tuple[typing.Any, ...]] = []
http_tests: list[tuple[typing.Any, ...]] = []
for path_ in pathlib.Path("tests/illformed").rglob("*.xml"):
    data_, text_ = get_file_contents(str(path_))
    if "http" in str(path_):
        info_ = (path_, data_, text_, *get_http_test_data(str(path_), data_, text_))
        http_tests.append(info_)
    else:
        info_ = (path_, data_, text_, *get_test_data(str(path_), text_))
        tests.append(info_)


@pytest.mark.parametrize("info", tests)
def test_strict_parser(info):
    path, data, text, description, eval_string, skip_unless = info
    try:
        eval(skip_unless, globals(), {})
    except (ModuleNotFoundError, ValueError):
        pytest.skip(description)
    result = feedparser.parse(data)
    assert eval(eval_string, {"datetime": datetime}, result), description
    assert everything_is_unicode(result)


@pytest.mark.parametrize("info", http_tests)
def test_http_conditions(info):
    path, data, text, url, description, eval_string, skip_unless = info
    result = feedparser.parse(url)
    assert result["bozo"] is True
    assert eval(eval_string, {"datetime": datetime}, result), description
    assert everything_is_unicode(result)
