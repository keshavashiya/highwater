# highwater

[![CI](https://github.com/keshavashiya/highwater/actions/workflows/ci.yml/badge.svg)](https://github.com/keshavashiya/highwater/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

By Keshav Ashiya

A surface-code decoder, instrumented as a real-time systems artefact.

The name is the high-water mark of the decode backlog: the highest the queue of
undecoded syndromes rises. A decoder slower than the cycle has no high-water
mark, because the queue never stops rising.

## Development

```bash
uv sync
just ci    # ruff check, ruff format --check, pytest: the same steps as CI
```

## License

MIT. See [LICENSE](LICENSE).
