"""Helpers for rich-text / HTML field content."""

from __future__ import annotations

import html
import re

from django.utils.html import strip_tags

# Zero-width / format characters that look empty but survive str.strip().
_INVISIBLE_CHARS_RE = re.compile(
    '[\u200b-\u200f\u202a-\u202e\u2060-\u2069\ufeff\u00ad]'
)
# Tags that end a paragraph-like block, and tags that end a single line.
_BLOCK_END_RE = re.compile(r'</\s*(?:p|div|h[1-6]|ul|ol|blockquote|pre)\s*>', re.IGNORECASE)
_LINE_BREAK_RE = re.compile(r'<\s*br\s*/?\s*>|</\s*li\s*>', re.IGNORECASE)
_LIST_ITEM_RE = re.compile(r'<\s*li(?:\s[^>]*)?>', re.IGNORECASE)
_EXTRA_BLANK_LINES_RE = re.compile(r'\n{3,}')


def is_empty_rich_text(value) -> bool:
    """Return True when value is empty or only whitespace / empty HTML tags."""
    if value is None:
        return True
    text = html.unescape(strip_tags(str(value)))
    text = _INVISIBLE_CHARS_RE.sub('', text).replace('\xa0', ' ').strip()
    return not text


def rich_text_to_plain_text(value) -> str:
    """Convert rich-text HTML to plain text, keeping paragraphs and line breaks.

    Used where HTML cannot be rendered, such as iCal descriptions.
    """
    if value is None:
        return ''
    text = _BLOCK_END_RE.sub('\n\n', str(value))
    text = _LINE_BREAK_RE.sub('\n', text)
    text = _LIST_ITEM_RE.sub('- ', text)
    text = html.unescape(strip_tags(text)).replace('\xa0', ' ')
    lines = [line.strip() for line in text.splitlines()]
    return _EXTRA_BLANK_LINES_RE.sub('\n\n', '\n'.join(lines)).strip()
