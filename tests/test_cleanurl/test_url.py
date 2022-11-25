import copy
from pathlib import Path

import pytest

from cleanurl import Url


class TestUrl:

    def test_scheme_property(self):
        scheme = 'ftp'
        url = Url(scheme=scheme)
        assert url.scheme == scheme
        with pytest.raises(AttributeError):
            url.scheme = 'new value'

    def test_username_property(self):
        username = 'value'
        url = Url(username=username)
        assert url.username == username
        with pytest.raises(AttributeError):
            url.username = 'new value'

    def test_password_property(self):
        password = 'value'
        url = Url(password=password)
        assert url.password == password
        with pytest.raises(AttributeError):
            url.password = 'new value'

    def test_path_property(self):
        path = Path('some/path')
        url = Url(path=path)
        assert url.path == path
        with pytest.raises(AttributeError):
            url.path = Path('new/value')

    def test_port_property(self):
        port = 8000
        url = Url(port=port)
        assert url.port == port
        with pytest.raises(AttributeError):
            url.port = 4200

    def test_host_property(self):
        host = 'iter-model'
        url = Url(host=host)
        assert url.host == host
        with pytest.raises(AttributeError):
            url.host = 'new-value'

    def test_query_property(self):
        query = {'param1': 'val1'}
        url = Url(query=query)
        assert url.query == query
        assert url._query is not query
        with pytest.raises(AttributeError):
            url.query = {'param2': 'val2'}

        # query view should be not mutable
        with pytest.raises(TypeError):
            url.query['param3'] = 'val3'

    @pytest.mark.parametrize(['url', 'result'], (
        (Url(), 'https://localhost/'),
        (Url(scheme='http'), 'http://localhost/'),
        (Url(host='www.google.com'), 'https://www.google.com/'),
        (Url(port=8000), 'https://localhost:8000/'),
        (Url(username='ubuntu'), 'https://localhost/'),
        (Url(password='root'), 'https://localhost/'),
        (Url(username='ubuntu', password='root'), 'https://ubuntu:root@localhost/'),
        (Url(path=Path('/api/user/get')), 'https://localhost/api/user/get'),
        (Url(path=Path('api/user/get')), 'https://localhost/api/user/get'),
        (Url(query={'param1': 'val1'}), 'https://localhost/?param1=val1'),
        (Url(query={'param1': 'val1', 'param2': 'val2'}), 'https://localhost/?param1=val1&param2=val2'),
        (
            Url(
                scheme='ftp',
                host='myhost',
                port=21,
                username='ubuntu',
                password='admin',
                path=Path('home/ubuntu/items.csv'),
                query={'param1': 'val1'},
            ),
            'ftp://ubuntu:admin@myhost:21/home/ubuntu/items.csv?param1=val1',
        ),
    ))
    def test_query_to_str(self, url: Url, result: str):
        assert str(url) == result

    def test_repr(self):
        url = Url(
            scheme='ftp',
            host='myhost',
            port=21,
            username='ubuntu',
            password='admin',
            path=Path('home/ubuntu/items.csv'),
            query={'param1': 'val1'},
        )
        assert repr(url) == "Url.parse('ftp://ubuntu:admin@myhost:21/home/ubuntu/items.csv?param1=val1')"

    def test_copy(self):
        url = Url(
            scheme='ftp',
            host='myhost',
            port=21,
            username='ubuntu',
            password='admin',
            path=Path('home/ubuntu/items.csv'),
            query={'param1': 'val1'},
        )

        copied_url = copy.copy(url)

        assert url.scheme == copied_url.scheme
        assert url.host == copied_url.host
        assert url.port == copied_url.port
        assert url.username == copied_url.username
        assert url.password == copied_url.password
        assert url.path == copied_url.path
        assert url.query == copied_url.query

        assert url.query is not copied_url.query

    def test_hash(self):
        url = Url(
            scheme='ftp',
            host='myhost',
            port=21,
            username='ubuntu',
            password='admin',
            path=Path('home/ubuntu/items.csv'),
            query={'param1': 'val1'},
        )
        assert hash(url) == hash(str(url))

    def test_eq(self):
        assert Url(host='ftp', port=23) == Url(host='ftp', port=23)
        assert Url(username='ubuntu') == Url(username='root')
        assert Url(password='ubuntu') == Url(password='root')
        assert Url(username='ubuntu', password='root') == Url(username='ubuntu', password='root')
        assert Url(username='ubuntu', password='root') != Url(username='ubuntu', password='roo2')

        assert not Url() == 'https://localhost'
        assert Url() != 'https://localhost'

    @pytest.mark.parametrize(('path', 'result'), (
        (Path('root/'), Path('root')),
        (Path('/root'), Path('root')),
        (None, None),
    ))
    def test__normalize_path(self, path: Path | None, result: Path | None):
        assert Url._normalize_path(path) == result

    @pytest.mark.parametrize(('base_url', 'path', 'final_url'), (
        (Url(), Path('/api/user/port'), Url(path=Path('/api/user/port'))),
        (Url(), Path('api/user/port'), Url(path=Path('api/user/port'))),
        (Url(path=Path('api/user')), Path('port'), Url(path=Path('api/user/port'))),
        (Url(path=Path('api/user')), Path('/port'), Url(path=Path('api/user/port'))),
    ))
    def test_join_path(self, base_url: Url, path: Path, final_url: Url):
        assert base_url.join_path(path) == final_url

    @pytest.mark.parametrize(('base_url', 'query_update', 'final_url'), (
        (Url(), {'param1': 'val1'}, Url(query={'param1': 'val1'})),
        (Url(query={'param1': 'val1'}), {'param2': 'val2'}, Url(query={'param1': 'val1', 'param2': 'val2'})),
        (Url(query={'param1': 'val1'}), {'param1': 'val2'}, Url(query={'param1': 'val2'})),
    ))
    def test_update_query(self, base_url: Url, query_update: dict, final_url: Url):
        assert base_url.update_query(query_update) == final_url

    @pytest.mark.parametrize(('url', 'raw_url'), (
        (Url(), 'https://localhost/'),
        (Url(scheme='http'), 'http://localhost/'),
        (Url(host='www.google.com'), 'https://www.google.com/'),
        (Url(port=8000), 'https://localhost:8000/'),
        (Url(username='ubuntu'), 'https://localhost/'),
        (Url(password='root'), 'https://localhost/'),
        (Url(username='ubuntu', password='root'), 'https://ubuntu:root@localhost/'),
        (Url(path=Path('/api/user/get')), 'https://localhost/api/user/get'),
        (Url(path=Path('api/user/get')), 'https://localhost/api/user/get'),
        (Url(query={'param1': 'val1'}), 'https://localhost/?param1=val1'),
        (Url(query={'param1': 'val1', 'param2': 'val2'}), 'https://localhost/?param1=val1&param2=val2'),
        (
            Url(
                scheme='ftp',
                host='myhost',
                port=21,
                username='ubuntu',
                password='admin',
                path=Path('home/ubuntu/items.csv'),
                query={'param1': 'val1'},
            ),
            'ftp://ubuntu:admin@myhost:21/home/ubuntu/items.csv?param1=val1',
        ),
    ))
    def test_parse(self, url: Url, raw_url: str):
        assert Url.parse(raw_url) == url

    @pytest.mark.parametrize(('url', 'result'), (
        (Url(username='ubuntu'), False),
        (Url(password='root'), False),
        (Url(password='ubuntu', username='root'), True),
    ))
    def test_contains_auth(self, url: Url, result: bool):
        assert url.contains_auth is result
