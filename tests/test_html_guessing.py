"""Exercise the HTML sniffing code"""

import pytest

import feedparser.mixin


@pytest.mark.parametrize(
    "input_text, expected_result, test_name",
    (
        ("plain text", False, "plain text"),
        ("2 < 3", False, "plain text with angle bracket"),
        ('<a href="">a</a>', True, "anchor tag"),
        ("<i>i</i>", True, "italics tag"),
        ("<b>b</b>", True, "bold tag"),
        ("<code>", False, "allowed tag, no end tag"),
        ("<rss> .. </rss>", False, "disallowed tag"),
        ("AT&T", False, "corporation name"),
        ("&copy;", True, "named entity reference"),
        ("&#169;", True, "numeric entity reference"),
        ("&#xA9;", True, "hex numeric entity reference"),
    ),
)
def test_html_guessing(input_text, expected_result, test_name):
    guess_result = bool(feedparser.mixin.XMLParserMixin.looks_like_html(input_text))
    assert guess_result is expected_result
