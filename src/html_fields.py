"""Extract HTML titles, text, and meaningful links, omitting media and hidden content.

No network, script execution, file selection, or domain-specific interpretation.
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path


# Static extraction only: external CSS and JavaScript are not evaluated.
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'}
OMIT = {'script', 'style', 'template', 'noscript', 'img', 'picture', 'video',
        'audio', 'source', 'track', 'svg', 'canvas', 'iframe', 'object', 'embed'}


class Fields(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values, self.titles, self.text = [], [], []
        self.stack = []
        self.pending = []

    def flush_text(self):
        text = ''.join(self.pending).strip()
        self.pending.clear()
        if text:
            self.values.append(text)
            self.text.append(text)
            if any(tag == 'title' for tag, _ in self.stack):
                self.titles.append(text)

    def handle_starttag(self, tag, attrs):
        self.flush_text()
        attrs = dict(attrs)
        styles = dict(item.split(':', 1) for item in (attrs.get('style') or '').lower().split(';')
                      if ':' in item)
        styles = {key.strip(): value.replace('!important', '').strip()
                  for key, value in styles.items()}
        hidden = (bool(self.stack and self.stack[-1][1]) or tag in OMIT
                  or 'hidden' in attrs or (attrs.get('aria-hidden') or '').lower() == 'true'
                  or styles.get('display') == 'none'
                  or styles.get('visibility') in ('hidden', 'collapse'))
        if not hidden:
            # Keep only meaningful labels and links, never arbitrary attributes.
            for key in ('title', 'href', 'download'):
                value = attrs.get(key)
                if value and not value.lstrip().lower().startswith(('data:', 'blob:', 'javascript:')):
                    self.values.append(value)
            if tag == 'meta' and attrs.get('property') == 'og:title':
                value = attrs.get('content')
                if value:
                    self.titles.append(value)
        if tag not in VOID:
            self.stack.append((tag, hidden))

    def handle_endtag(self, tag):
        self.flush_text()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, text):
        if not self.stack or not self.stack[-1][1]:
            self.pending.append(text)


def read_fields(value):
    path = Path(value)
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'Expected a regular HTML file: {path}')
    parser = Fields()
    with path.open(encoding='utf-8', errors='replace') as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), ''):
            parser.feed(chunk)
    parser.close()
    parser.flush_text()
    return {'path': str(path), 'titles': list(dict.fromkeys(parser.titles)),
            'values': list(dict.fromkeys(parser.values)), 'text': parser.text}


if __name__ == '__main__':
    try:
        print(json.dumps([read_fields(path) for path in sys.argv[1:]]))
    except (OSError, ValueError) as error:
        sys.exit(f'STOP: {error}')
