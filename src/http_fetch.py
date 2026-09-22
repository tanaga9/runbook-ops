"""Bounded HTTP GET; callers own interpretation, persistence, and failure policy."""
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


class FetchError(Exception):
    def __init__(self, reason, status=None, retry_after=None):
        super().__init__(reason)
        self.status = status
        self.retry_after = retry_after


def fetch_bytes(url, *, headers=None, timeout=30, max_bytes=4 * 1024 * 1024,
                attempts=1, retry_statuses=(), retry_network=False, delay=0):
    """Return bytes from HTTP 200 or raise FetchError / ValueError.

    Only explicitly selected failures are retried. Retry-After is reported to
    the caller, not interpreted as permission to retry. No files are written.
    """
    if attempts < 1 or timeout <= 0 or max_bytes < 1 or delay < 0:
        raise ValueError('Invalid HTTP limits')
    if urllib.parse.urlsplit(url).scheme not in ('http', 'https'):
        raise ValueError('Expected an HTTP(S) URL')
    request = urllib.request.Request(url, headers=headers or {})
    for attempt in range(1, attempts + 1):
        print(f'GET ({attempt}/{attempts}): {url}', file=sys.stderr, flush=True)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if response.status != 200:
                    raise FetchError(f'Unexpected HTTP {response.status}', response.status)
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ValueError(f'Response exceeds {max_bytes} bytes')
                return data
        except urllib.error.HTTPError as error:
            failure = FetchError(f'HTTP {error.code}: {error.reason}', error.code,
                                 error.headers.get('Retry-After') if error.headers else None)
            error.close()
            retry = error.code in retry_statuses
        except (urllib.error.URLError, TimeoutError) as error:
            failure = FetchError(str(error))
            retry = retry_network
        print(f'Retrieval failed: {failure}', file=sys.stderr, flush=True)
        if not retry or attempt == attempts:
            raise failure
        time.sleep(delay)
