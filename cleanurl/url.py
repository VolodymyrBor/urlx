import copy
from pathlib import Path
from typing import TypeAlias

StrDict: TypeAlias = dict[str, str]


class Url:

    __slots__ = (
        '_port',
        '_path',
        '_username',
        '_password',
        '_host',
        '_port',
        '_scheme',
        '_query',
        '_cashed_build_url',
    )

    def __init__(
        self,
        *,
        scheme: str = 'https',
        host: str = 'localhost',
        username: str | None = None,
        password: str | None = None,
        path: Path = Path('/'),
        port: int | None = None,
        query: StrDict | None = None,
    ):
        self._port = port
        self._path = path
        self._password = password
        self._username = username
        self._host = host
        self._scheme = scheme
        self._query: dict = {} if query is None else query

        self._cashed_build_url: str | None = None

    @classmethod
    def parse(cls, raw_url: str) -> 'Url':
        scheme, raw_url = raw_url.split('://', 1)
        username, password = None, None
        if '@' in raw_url:
            username_password, raw_url = raw_url.split('@', 1)
            username, password = username_password.split(':', 1)

        host, raw_url = raw_url.split('/', 1)

        port = None
        if ':' in host:
            host, port = host.split(':', 1)
            port = int(port)

        query = {}
        if '?' in raw_url:
            path_part, query_part = raw_url.split('?', 1)
            path = Path(path_part)
            query = dict(
                part.split('=', 1)
                for part in query_part.split('&')
            )
        else:
            path = Path(raw_url)

        return Url(
            scheme=scheme,
            username=username,
            password=password,
            host=host,
            port=port,
            path=path,
            query=query,
        )

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def username(self) -> str | None:
        return self._username

    @property
    def password(self) -> str | None:
        return self._password

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int | None:
        return self._port

    @property
    def path(self) -> Path:
        return self._path

    @property
    def query(self) -> StrDict:
        return self._query

    def join_path(self, path: Path) -> 'Url':
        new_url = copy.copy(self)
        new_url._path = new_url._path.joinpath(path)
        return new_url

    def update_query(self, query: StrDict) -> 'Url':
        new_url = copy.copy(self)
        new_url._query.update(query)
        return new_url

    def _build_url(self) -> str:

        if self._cashed_build_url is not None:
            return self._cashed_build_url

        auth_part = f'{self._username}:{self._password}@' if self._password and self._username else ''
        port = f':{self._port}' if self._port else ''
        query_part = '?' + '&'.join(
            f'{key}={value}'
            for key, value in self._query.items()
        ) if self._query else ''
        build_url = f'{self._scheme}://{auth_part}{self._host}{port}/{self._path.as_posix()}{query_part}'
        self._cashed_build_url = build_url
        return build_url

    def __eq__(self, other: 'Url') -> bool | None:
        if not isinstance(other, Url):
            return NotImplemented

        return all((
            self.scheme == other.scheme,
            self.host == other.host,
            self.username == other.username,
            self.password == other.password,
            self.port == other.port,
            self.path == other.path,
            self.query == other.query,
        ))

    def __hash__(self) -> int:
        return hash(repr(self))

    def __copy__(self) -> 'Url':
        return Url(
            scheme=self._scheme,
            username=self._username,
            password=self._password,
            host=self._host,
            port=self._port,
            path=self._path,
            query=self._query.copy(),
        )

    def __str__(self) -> str:
        return self._build_url()

    def __repr__(self) -> str:
        cls = type(self)
        cls_name = cls.__name__
        method_name = cls.parse.__name__
        return f'{cls_name}.{method_name}({self._build_url()!r})'


if __name__ == '__main__':
    url = Url(
        scheme='http',
        host='127.0.0.1',
        port=8000,
        username='ubuntu',
        password='ubuntu',
        path=Path('api/net'),
        query={'query': 'books'},
    )
    print(url)
