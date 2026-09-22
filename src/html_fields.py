"""Read HTML as JSON fields: titles, attribute values, and text chunks.

No network, script execution, file selection, or domain-specific interpretation.
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path


class Fields(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values, self.titles = [], []
        self.hidden = False
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        self.hidden = self.hidden or tag in ('script', 'style')
        if self.hidden:
            return
        self.in_title = tag == 'title'
        self.values.extend(value for _, value in attrs if value)
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('property') == 'og:title':
            self.titles.append(attrs.get('content', ''))

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = False
        if tag == 'title':
            self.in_title = False

    def handle_data(self, text):
        if not self.hidden and text.strip():
            self.values.append(text.strip())
            if self.in_title:
                self.titles.append(text.strip())


def read_fields(value):
    path = Path(value)
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'Expected a regular HTML file: {path}')
    parser = Fields()
    parser.feed(path.read_text(encoding='utf-8', errors='replace'))
    parser.close()
    return {'path': str(path), 'titles': list(dict.fromkeys(parser.titles)),
            'values': list(dict.fromkeys(parser.values))}


if __name__ == '__main__':
    try:
        print(json.dumps([read_fields(path) for path in sys.argv[1:]]))
    except (OSError, ValueError) as error:
        sys.exit(f'STOP: {error}')
