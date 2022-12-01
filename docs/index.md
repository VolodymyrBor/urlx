# Home

## Overview

<figure markdown>
  ![cleanurl](img/icon.png){ width="300" align }
</figure>

<a href="https://pypi.org/project/cleanurl" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/cleanurl.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/cleanurl" target="_blank">
    <img src="https://img.shields.io/pypi/v/cleanurl?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://github.com/VolodymyrBor/cleanurl/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/VolodymyrBor/cleanurl/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>

[![Supported Versions](https://img.shields.io/badge/coverage-100%25-green)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/poetry-✅-grey)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/async-✅-grey)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/mypy-✅-grey)](https://shields.io/)

---

**cleanurl** - provide new data type - `Url`.
The purpose of this package is to standardize URL declaration in the codebase.
This approach should reduce the number of errors and speed up code writing.

---

## Installation

=== "PIP"

    ``` shell
    pip install cleanurl
    ```

=== "Poetry"

    ``` shell
    poetry add cleanurl
    ```

---

## Example

```python
from  pathlib import Path

from cleanurl import Url, Protocol, Port

url = Url(
    protocol=Protocol.HTTPS,
    host='localhost',
    port=Port.HTTPS,
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

**Source code**: [github.com/VolodymyrBor/cleanurl](https://github.com/VolodymyrBor/cleanurl)

**Documentation**: [cleanurl](https://volodymyrbor.github.io/cleanurl/)

**Changelog**: [changelog](https://volodymyrbor.github.io/cleanurl/changelog)
