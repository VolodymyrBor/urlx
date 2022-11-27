from enum import IntEnum


class Port(IntEnum):
    # HTTP
    HTTP = 80
    HTTPS = 443

    # Emails
    SMTP = 25
    SMTP_SSL_TLS = 465

    # FTP
    FTP_20 = 20
    FTP_21 = 20

    SSH = 22

    # Databases
    REDIS = 6379
    MY_SQL = 3306
    REDSHIFT = 5439
    POSTGRES_SQL = 5432

    # Queue services
    RMQ = 5672

    def __str__(self) -> str:
        return str(self.value)
