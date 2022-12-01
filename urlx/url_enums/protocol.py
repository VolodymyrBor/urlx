from urlx.strenum import StrEnum


class Protocol(StrEnum):
    # HTTP
    HTTP = 'http'
    HTTPS = 'https'

    # FTP
    FTP = 'ftp'
    FTPS = 'ftps'

    # Cloud storages
    S3 = 's3'
    GOOGLE_STORAGE = 'gs'

    # Advanced Message Queuing Protocol
    AMQP = 'amqp'

    # Websocket
    WEB_SOCKET = 'ws'

    # Databases
    REDIS = 'redis'
    POSTGRES = 'postgres'
    JAVA_CONNECTOR_MYSQL = 'jdbc:mysql'
    JAVA_CONNECTOR_REDSHIFT = 'jdbc:redshift'
