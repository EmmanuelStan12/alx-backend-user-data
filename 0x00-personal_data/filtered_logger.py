#!/usr/bin/env python3
"""
Module for Regexing
"""
import logging
from typing import List
import re
import mysql.connector


PPI_FIELDS = ("name", "email", "phone", "ssn", "password")
extract = lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y)
replace = lambda x: r'\g<field>={}'.format(x)


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        seperator: str
) -> str:
    """Use a regex to replace occurrences for values
    """
    return re.sub(extract(fields, seperator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Logger that logs up to logging.INFO
    """
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter[PPI_FIELDS])
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a database
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    conn = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_password,
            database=db_name
    )
    return conn


def main() -> None:
    """Retrieves row from a db and logs it.
    """
    cols = ["name", "email", "phone", "ssn",
              "password", "ip", "last_login", "user_agent"]
    fields = ','.join(cols)
    query = "SELECT {} FROM users;".format(fields)
    logger = get_logger()
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = '; '.join(
                [f"{columns[i]}={row[i]}" for i in range(len(row))]
            )
            msg = '{};'.format(record)
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record
        """
        msg = super(RedactingFormatter, self).format(record)
        result = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return result
