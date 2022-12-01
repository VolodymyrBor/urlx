from enum import IntEnum

from urlx.strenum import Enum2Str


class Port(IntEnum, Enum2Str):
    # HTTP
    HTTP_80 = 80
    HTTPS_443 = 443

    # Emails
    SMTP_25 = 25
    SMTP_SSL_TLS_465 = 465

    # FTP
    FTP_20 = 20
    FTP_21 = 21

    SSH_22 = 22

    # Databases
    REDIS_6379 = 6379
    MY_SQL_3306 = 3306
    REDSHIFT_5439 = 5439
    POSTGRES_SQL_5432 = 5432

    # Queue services
    RMQ_5672 = 5672
