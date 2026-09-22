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
            page.write_text('<title>Report</title><a href="report.pdf">A &amp; B</a><script>hidden</script>')
            result = html.read_fields(page)
            self.assertEqual(result['titles'], ['Report'])
            self.assertIn('report.pdf', result['values'])
            self.assertIn('A & B', result['values'])
            self.assertNotIn('hidden', result['values'])
