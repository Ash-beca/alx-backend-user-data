#!/usr/bin/env python3
"""Module defines `filter_datum` function
"""
import logging
import mysql.connector
from os import environ
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        """Initialize"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Extended format function from parent class"""
        return filter_datum(
            self.fields, self.REDACTION,
            logging.Formatter.format(self, record),
            self.SEPARATOR,
        )


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Return log message obfuscated

    Args:
        fields: list of strings representing all fields to obfuscate
        redaction: string representing by what the field will be obfuscated
        message: string representing the log line
        separator: string representing by which character is separating all
        fields in the log line (message)

    Returns:
        obfuscated log message
    """
    return re.sub(
            r'({})=(.*?){}'.format('|'.join(fields), separator),
            r'\1={}'.format(redaction), message
        )


def get_logger() -> logging.Logger:
    """Return logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(sh)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a database connector object"""
    return mysql.connector.connect(
        user=environ.get("PERSONAL_DATA_DB_USERNAME"),
        password=environ.get("PERSONAL_DATA_DB_PASSWORD"),
        host=environ.get("PERSONAL_DATA_DB_HOST"),
        database=environ.get("PERSONAL_DATA_DB_NAME")
    )


def main() -> None:
    """Logs redacted recrods from MySQL database"""
    con = get_db()  # Get connection to database
    cur = con.cursor()  # Get a cursor object from mysql shell
    query = "SELECT * FROM users;"  # Construct a query
    cur.execute(query)  # Execute query in and get response object

    # Get column names in a list
    col = list(map(lambda row: row[0], cur.description))
    message = []
    logger = get_logger()

    # construct `column_name`=`data` list for each row and append to message
    try:
        for row in cur.fetchall():
            message.append('; '.join(list(map(
                    lambda name, value: name+'='+str(value), col, row
                ))))
    except Exception as e:
        print(e)
    finally:
        con.close()
    for msg in message:
        logger.info(msg)


if __name__ == "__main__":
    main()
