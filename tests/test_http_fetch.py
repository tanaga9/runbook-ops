"""Test HTTP mechanics without contacting external services."""
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

spec = importlib.util.spec_from_file_location('http_fetch', Path(__file__).resolve().parents[1] / 'src/http_fetch.py')
http = importlib.util.module_from_spec(spec)
spec.loader.exec_module(http)


def response(data=b'{}'):
    result = io.BytesIO(data)
    result.status = 200
    return result


class HttpFetchTests(unittest.TestCase):
    def setUp(self):
        self.stderr = patch('sys.stderr', new_callable=io.StringIO).start()
        self.request = patch.object(http.urllib.request, 'urlopen').start()
        self.sleep = patch.object(http.time, 'sleep').start()
        self.addCleanup(patch.stopall)

    def test_success_preserves_headers_and_limits(self):
        self.request.return_value = response()
        self.assertEqual(http.fetch_bytes('https://example.test', headers={'User-Agent': 'test'},
                                         timeout=7, max_bytes=2), b'{}')
        self.assertEqual(self.request.call_args.args[0].get_header('User-agent'), 'test')
        self.assertEqual(self.request.call_args.kwargs['timeout'], 7)
        self.sleep.assert_not_called()

    def test_selected_status_retries_then_succeeds(self):
        self.request.side_effect = [HTTPError('url', 404, 'Missing', {}, None), response()]
        self.assertEqual(http.fetch_bytes('https://example.test', attempts=3,
                                         retry_statuses=(404,), delay=10), b'{}')
        self.sleep.assert_called_once_with(10)

    def test_denial_and_rate_limit_are_reported_without_retry(self):
        for code in (403, 429):
            self.request.reset_mock()
            self.request.side_effect = HTTPError('url', code, 'Denied', {'Retry-After': '60'}, None)
            with self.assertRaises(http.FetchError) as caught:
                http.fetch_bytes('https://example.test', attempts=3, retry_statuses=(404,))
            self.assertEqual(caught.exception.status, code)
            self.assertEqual(caught.exception.retry_after, '60')
            self.assertEqual(self.request.call_count, 1)
        self.sleep.assert_not_called()

    def test_network_retry_is_opt_in_and_bounded(self):
        for failure in (URLError('offline'), TimeoutError('timeout')):
            for retry, count in ((False, 1), (True, 3)):
                self.request.reset_mock()
                self.sleep.reset_mock()
                self.request.side_effect = failure
                with self.assertRaises(http.FetchError) as caught:
                    http.fetch_bytes('https://example.test', attempts=3, retry_network=retry)
                self.assertIsNone(caught.exception.status)
                self.assertEqual(self.request.call_count, count)
                self.assertEqual(self.sleep.call_count, count - 1)

    def test_oversized_response_stops_without_retry(self):
        self.request.return_value = response(b'1234')
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            http.fetch_bytes('https://example.test', max_bytes=3, attempts=3)
        self.assertEqual(self.request.call_count, 1)
        self.sleep.assert_not_called()

    def test_invalid_configuration_does_not_request(self):
        for kwargs in ({'attempts': 0}, {'timeout': 0}, {'max_bytes': 0}, {'delay': -1}):
            with self.assertRaises(ValueError):
                http.fetch_bytes('https://example.test', **kwargs)
        with self.assertRaises(ValueError):
            http.fetch_bytes('file:///etc/hosts')
        self.request.assert_not_called()
