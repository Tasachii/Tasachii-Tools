<!--
STYLE EXEMPLAR (archetype: serious OSS library, Python).
Shows the house style scaled up for a PUBLIC open-source project: a table-of-contents
(the README is long enough to need one), real badges, and the sibling-file conventions
that a contributed-to project needs — Contributing, Security, Code of Conduct, Support.
A different language (Python) on purpose, to show the style is not Node-only.
Copy the SHAPE and the conventions, never the facts.
-->

# retryable

A tiny, typed retry decorator for Python. Wrap any function and it re-runs on failure with
exponential backoff and jitter, configurable stop conditions, and a hook for logging each
attempt. Pure standard library, sync and async, fully type-annotated.

[![PyPI](https://img.shields.io/pypi/v/retryable)](https://pypi.org/project/retryable/)
[![CI](https://img.shields.io/github/actions/workflow/status/Tasachii/retryable/ci.yml)](https://github.com/Tasachii/retryable/actions)
[![Coverage](https://img.shields.io/codecov/c/github/Tasachii/retryable)](https://app.codecov.io/gh/Tasachii/retryable)
[![Python](https://img.shields.io/pypi/pyversions/retryable)](https://pypi.org/project/retryable/)
[![License](https://img.shields.io/pypi/l/retryable)](LICENSE)

## Contents

- [Quickstart](#quickstart)
- [Why this exists](#why-this-exists)
- [API](#api)
- [Recipes](#recipes)
- [Compatibility](#compatibility)
- [Contributing](#contributing)
- [Security](#security)
- [Support](#support)
- [License](#license)

## Quickstart

```bash
pip install retryable
```

```python
from retryable import retry

@retry(attempts=5, on=ConnectionError)
def fetch(url: str) -> bytes:
    ...  # re-runs up to 5 times on ConnectionError, backing off between tries
```

Async works the same way — `@retry` detects a coroutine and awaits it.

## Why this exists

Retry logic is easy to write badly: a bare `for` loop with `time.sleep` has no jitter
(so every client retries in lockstep and hammers a recovering service), no cap on total
wait, and no way to retry on some exceptions but not others. `retryable` is that logic
written once, tested against those edge cases, in ~200 lines with no dependencies.

## API

| Parameter | Type | Default | Description |
|---|---|---|---|
| `attempts` | `int` | `3` | Maximum number of calls, including the first. |
| `on` | `type[Exception] \| tuple[...]` | `Exception` | Which exceptions trigger a retry. Anything else propagates immediately. |
| `backoff` | `float` | `0.5` | Base seconds for exponential backoff (`base * 2 ** n`). |
| `jitter` | `bool` | `True` | Add random 0–`backoff` seconds so clients don't retry in lockstep. |
| `max_delay` | `float \| None` | `None` | Cap on any single sleep, in seconds. |
| `on_retry` | `Callable[[RetryState], None] \| None` | `None` | Called before each re-attempt — use it to log. |

When all attempts are exhausted the **last** exception is re-raised unchanged.

## Recipes

```python
# Log every retry
@retry(attempts=4, on_retry=lambda s: log.warning("retry %d after %s", s.attempt, s.error))
def call(): ...

# Retry several error types, cap the wait
@retry(on=(TimeoutError, ConnectionError), backoff=1.0, max_delay=10.0)
async def pull(): ...
```

## Compatibility

- Python 3.9 or newer
- No runtime dependencies; ships `py.typed` for full type-checker support
- Works with both `def` and `async def` functions

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the dev setup,
test commands, and the pull-request checklist. By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md).

```bash
git clone https://github.com/Tasachii/retryable.git
cd retryable
pip install -e ".[dev]"
pytest
```

## Security

Please do not open public issues for vulnerabilities. The reporting process and supported
versions are described in [SECURITY.md](SECURITY.md).

## Support

- Questions and ideas → [GitHub Discussions](https://github.com/Tasachii/retryable/discussions)
- Bugs and feature requests → [Issues](https://github.com/Tasachii/retryable/issues)

## License

MIT © Phasathat Jaruchitsophon
