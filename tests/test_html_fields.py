"""HTML decoding is domain-independent; interpretation belongs to callers."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('html_fields', Path(__file__).resolve().parents[1] / 'src/html_fields.py')
html = importlib.util.module_from_spec(spec)
spec.loader.exec_module(html)


class HtmlFieldsTests(unittest.TestCase):
    def test_fields_entities_titles_and_scripts(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / 'page.html'
            page.write_text('<title>Report</title><a href="report.pdf">A &amp; B</a><script>hidden</script><div class="changing-name"><span>Label</span><p>Value</p><span>Label</span></div>')
            result = html.read_fields(page)
            self.assertEqual(result['titles'], ['Report'])
            self.assertIn('report.pdf', result['values'])
            self.assertIn('A & B', result['values'])
            self.assertNotIn('hidden', result['values'])
            self.assertEqual(result['text'], ['Report', 'A & B', 'Label', 'Value', 'Label'])

    def test_media_hidden_content_and_large_attributes_are_omitted(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / 'media.html'
            page.write_text(
                '<title>Visible report</title><!-- secret-comment -->'
                '<img src="data:image/png;base64,' + 'A' * 200000 + '">'
                '<video><source src="movie.mp4">secret-video</video>'
                '<svg><text>secret-vector</text></svg>'
                '<iframe src="frame.html">secret-frame</iframe>'
                '<div hidden><span>secret-hidden</span><script>secret-script</script>'
                '<p>secret-nested</p></div>'
                '<p style="DISPLAY: none !important">secret-style</p>'
                '<p aria-hidden="true">secret-aria</p>'
                '<template>secret-template</template>'
                '<a href="data:video/mp4;base64,secret-data">Visible link</a>'
                '<div class="private-class" data-payload="secret-payload">'
                '<span>Base Model</span><p>Example</p></div>'
                '<a href="model.safetensors">Download</a>')
            result = html.read_fields(page)
            rendered = str(result)
            self.assertNotIn('secret-', rendered)
            self.assertNotIn('private-class', rendered)
            self.assertNotIn('data:', rendered)
            self.assertLess(len(rendered), 1000)
            self.assertEqual(result['text'],
                             ['Visible report', 'Visible link', 'Base Model', 'Example', 'Download'])
            self.assertIn('model.safetensors', result['values'])

    def test_chunked_text_keeps_words_intact(self):
        parser = html.Fields()
        for chunk in ('<p>Vis', 'ible &am', 'p; useful', '</p><img/><p>After</p>'):
            parser.feed(chunk)
        parser.close()
        parser.flush_text()
        self.assertEqual(parser.text, ['Visible & useful', 'After'])
