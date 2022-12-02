<p align="center">
    <a href="https://volodymyrbor.github.io/urlx">
        <img src="https://volodymyrbor.github.io/urlx/img/icon.png" alt="urlx" width="300">
    </a>
</p>

# UrlX

<a href="https://pypi.org/project/urlx" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/urlx.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/urlx" target="_blank">
    <img src="https://img.shields.io/pypi/v/urlx?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://github.com/VolodymyrBor/urlx/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/VolodymyrBor/urlx/actions/workflows/build.yml/badge.svg?event=push&branch=main" alt="Build">
</a>

[![Supported Versions](https://img.shields.io/badge/coverage-100%25-green)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/poetry-✅-grey)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/mypy-✅-grey)](https://shields.io/)

---

**urlx** - provide new data type - `Url`.
The purpose of this package is to standardize URL declaration in the codebase.
This approach should reduce the number of errors and speed up code writing.

---

## Example

```python
from pathlib import Path

from urlx import Url, Protocol, Port

url = Url(
    protocol=Protocol.HTTPS,
    host='localhost',
    port=Port.HTTPS_443,
    path=Path('api/user-list'),
    query={
        'limit': '100',
        'skip': '20',
    },
)
print(url)
```
Output: 

> https://localhost:443/api/user-list?limit=100&skip=20

---

## Links

**Source code**: [github.com/VolodymyrBor/urlx](https://github.com/VolodymyrBor/urlx)

**Documentation**: [urlx](https://volodymyrbor.github.io/urlx/)

**Changelog**: [changelog](https://volodymyrbor.github.io/urlx/changelog)
