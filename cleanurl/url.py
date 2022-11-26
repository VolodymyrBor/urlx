import copy
from pathlib import Path
from typing import TypeAlias
from types import MappingProxyType

StrDict: TypeAlias = dict[str, str]

_EMPTY = object()


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
    )

    def __init__(
        self,
        *,
        scheme: str = 'https',
        host: str = 'localhost',
        username: str | None = None,
        password: str | None = None,
        path: Path = Path(''),
        port: int | None = None,
        query: StrDict | None = None,
    ):
        self._port = port
        self._path = self._normalize_path(path)
        self._password = password
        self._username = username
        self._host = host
        self._scheme = scheme
        self._query: dict = {} if query is None else copy.copy(query)

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
    def query(self) -> MappingProxyType[str, str]:
        return MappingProxyType(self._query)

    @property
    def contains_auth(self) -> bool:
        return all((
            self.username is not None,
            self.password is not None,
        ))

    def join_path(self, path: Path) -> 'Url':
        new_url = copy.copy(self)
        new_url._path = new_url._path.joinpath(self._normalize_path(path))
        return new_url

    def update_query(self, query: StrDict) -> 'Url':
        new_url = copy.copy(self)
        new_url._query.update(query)
        return new_url

    def copy_with(
        self,
        scheme: str = _EMPTY,
        host: str = _EMPTY,
        port: int | None = _EMPTY,
        username: str | None = _EMPTY,
        password: str | None = _EMPTY,
        path: Path = _EMPTY,
        query: dict = _EMPTY,
    ) -> 'Url':
        copied_url = copy.copy(self)

        if scheme is not _EMPTY:
            copied_url._scheme = scheme
        if host is not _EMPTY:
            copied_url._host = host
        if port is not _EMPTY:
            copied_url._port = port
        if username is not _EMPTY:
            copied_url._username = username
        if password is not _EMPTY:
            copied_url._password = password
        if path is not _EMPTY:
            copied_url._path = path
        if query is not _EMPTY:
            copied_url._query = query

        return copied_url

    def build(self, secure_password: bool = False) -> str:
        auth_part = ''
        if self._password and self._username:
            password = '<password>' if secure_password else self._password
            auth_part = f'{self._username}:{password}@'

        port = f':{self._port}' if self._port else ''
        query_part = '?' + '&'.join(
            f'{key}={value}'
            for key, value in self._query.items()
        ) if self._query else ''
        path_part = '' if self._path == Path('') else self._path.as_posix()
        return f'{self._scheme}://{auth_part}{self._host}{port}/{path_part}{query_part}'

    @staticmethod
    def _normalize_path(path: Path | None) -> Path | None:
        if path is None:
            return None
        return Path(str(path).strip('/\\'))

    def __eq__(self, other: 'Url') -> bool | None:
        if not isinstance(other, Url):
            return NotImplemented

        return all((
            self.scheme == other.scheme,
            self.host == other.host,
            (
                self.username == other.username
                and self.password == other.password
            ) if self.contains_auth else True,
            self.port == other.port,
            self.path == other.path,
            self.query == other.query,
        ))

    def __hash__(self) -> int:
        return hash(str(self))

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
        return self.build()

    def __repr__(self) -> str:
        cls = type(self)
        cls_name = cls.__name__
        method_name = cls.parse.__name__
        return f'{cls_name}.{method_name}({self.build()!r})'
