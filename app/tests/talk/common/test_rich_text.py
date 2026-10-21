import pytest

from eventyay.common.text.rich_text import is_empty_rich_text, rich_text_to_plain_text


@pytest.mark.parametrize(
    ('value', 'expected'),
    (
        (None, True),
        ('', True),
        ('   ', True),
        ('<p></p>', True),
        ('<p><br></p>', True),
        ('<p>&nbsp;</p>', True),
        ('<p> </p>', True),
        ('<p>\u200b</p>', True),
        ('\u200b\u200c\ufeff', True),
        ('<p>Hi</p>', False),
        ('Hi', False),
        ('<p>Hi\u200b</p>', False),
    ),
)
def test_is_empty_rich_text(value, expected):
    assert is_empty_rich_text(value) is expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    (
        (None, ''),
        ('', ''),
        ('Plain text', 'Plain text'),
        ('<p>One</p><p>Two</p>', 'One\n\nTwo'),
        ('<p>Line one<br>Line two</p>', 'Line one\nLine two'),
        ('<ul><li>First</li><li>Second</li></ul>', '- First\n- Second'),
        ('<p>Tom &amp; Jerry&nbsp;rock</p>', 'Tom & Jerry rock'),
        ('<p><strong>Bold</strong> and <a href="https://example.com">link</a></p>', 'Bold and link'),
        ('<p></p><p>Text</p><p></p>', 'Text'),
    ),
)
def test_rich_text_to_plain_text(value, expected):
    assert rich_text_to_plain_text(value) == expected
