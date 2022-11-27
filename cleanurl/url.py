import copy
from pathlib import Path
from typing import TypeAlias, Any
from types import MappingProxyType

from .url_enums import Protocol, Port

StrDict: TypeAlias = dict[str, str]
_PORT_T: TypeAlias = Port | int | None
_PROTOCOL_T: TypeAlias = Protocol | str

_EMPTY = object()


class Url:

    __slots__ = (
        '_port',
        '_path',
        '_username',
        '_password',
        '_host',
        '_port',
        '_protocol',
        '_query',
    )

    def __init__(
        self,
        *,
        protocol: _PROTOCOL_T = Protocol.HTTPS,
        host: str = 'localhost',
        username: str | None = None,
        password: str | None = None,
        path: Path = Path(''),
        port: _PORT_T = None,
        query: StrDict | None = None,
    ):
        self._port = port
        self._path = self._normalize_path(path)
        self._password = password
        self._username = username
        self._host = host
        self._protocol = protocol
        self._query: dict = {} if query is None else copy.copy(query)

    @classmethod
    def parse(cls, raw_url: str) -> 'Url':
        """Parse string-url to `Url`

        :param raw_url: string url
        :return: parsed `Url`
        """
        protocol, raw_url = raw_url.split('://', 1)
        username, password = None, None
        if '@' in raw_url:
            username_password, raw_url = raw_url.split('@', 1)
            username, password = username_password.split(':', 1)

        host, raw_url = raw_url.split('/', 1)

        port = None
        if ':' in host:
            host, raw_port = host.split(':', 1)
            port = int(raw_port)

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
            protocol=protocol,
            username=username,
            password=password,
            host=host,
            port=port,
            path=path,
            query=query,
        )

    @property
    def protocol(self) -> _PROTOCOL_T:
        """Protocol getter

        :return: `protocol`
        """
        return self._protocol

    @property
    def username(self) -> str | None:
        """Username getter

        :return: `username`
        """
        return self._username

    @property
    def password(self) -> str | None:
        """Password getter

        :return: `password`
        """
        return self._password

    @property
    def host(self) -> str:
        """Host getter

        :return: `host`
        """
        return self._host

    @property
    def port(self) -> _PORT_T:
        """Port getter

        :return: `port`
        """
        return self._port

    @property
    def path(self) -> Path:
        """Path getter

        :return: url path
        """
        return self._path

    @property
    def query(self) -> MappingProxyType[str, str]:
        """Query getter

        :return: unmodifiable view of query
        """
        return MappingProxyType(self._query)

    @property
    def contains_auth(self) -> bool:
        """Check that url contains auth part

        :return: True if `username` and `password` are not None
        """
        return all((
            self.username is not None,
            self.password is not None,
        ))

    def join_path(self, path: Path) -> 'Url':
        """Join path to url

        :param path: additional path
        :return: new url
        """
        new_url = copy.copy(self)
        new_url._path = new_url._path.joinpath(self._normalize_path(path))
        return new_url

    def update_query(self, query: StrDict) -> 'Url':
        """Update query part of the url

        :param query: dict of query parameters
        :return: new url
        """
        new_url = copy.copy(self)
        new_url._query.update(query)
        return new_url

    def copy_with(
        self,
        protocol: _PROTOCOL_T = _EMPTY,  # type: ignore
        host: str = _EMPTY,  # type: ignore
        port: _PORT_T = _EMPTY,  # type: ignore
        username: str | None = _EMPTY,  # type: ignore
        password: str | None = _EMPTY,  # type: ignore
        path: Path = _EMPTY,  # type: ignore
        query: dict = _EMPTY,  # type: ignore
    ) -> 'Url':
        """Copy url with new attributes

        :param protocol: scheme
        :param host: host
        :param port: port
        :param username: username
        :param password: password
        :param path: path
        :param query: query
        :return: new url
        """
        copied_url = copy.copy(self)

        if protocol is not _EMPTY:
            copied_url._protocol = protocol
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
        """Build str-representation of the url

        :param secure_password: `password` will be hidden if it's `True`
        :return: str-representation of the url
        """
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
        return f'{self._protocol}://{auth_part}{self._host}{port}/{path_part}{query_part}'

    @staticmethod
    def _normalize_path(path: Path) -> Path:
        """Normalized path - remove extra symbols like slash

        :param path: path
        :return: normalized path
        """
        return Path(str(path).strip('/\\'))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Url):
            return NotImplemented

        return all((
            self.protocol == other.protocol,
            self.host == other.host,
            (
                self.username == other.username
                and self.password == other.password  # pragma: no cover
            ) if self.contains_auth else True,
            self.port == other.port,
            self.path == other.path,
            self.query == other.query,
        ))

    def __hash__(self) -> int:
        return hash(str(self))

    def __copy__(self) -> 'Url':
        return Url(
            protocol=self._protocol,
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
