#!/usr/bin/env python3
""" Redacting Formatter class
"""
import os
import re
from typing import List
import logging
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "address", "ssn")

# CLASSES
""" Redacting Formatter class
"""


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)

# METHODS


"""returns the log message obfuscated"""


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    p = fr'(\b|{re.escape(separator)})({"|".join(map(re.escape, fields))})=([^;]+)'
    return re.sub(p, lambda match: f'{match.group(1)}{match.group(2)}={redaction}', message)


def get_logger() -> logging.Logger:
    """Return a configured logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger


"""Return a MySQLConnection object to connect to the database"""


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a MySQLConnection object to connect to the database"""
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    name = os.environ.get('PERSONAL_DATA_DB_NAME', '')

    try:
        connection = mysql.connector.connect(
            user=username,
            password=passwd,
            host=db_host,
            database=name
        )
        return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


"""is the only one that runs when the module is executed"""


def main():
    """is the only one that runs when the module is executed"""
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = get_logger(formatter)

    db_connection = get_db()

    if db_connection:
        try:
            cursor = db_connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()

            for row in results:
                filtered_data = {field: '***' for field in PII_FIELDS}
                filtered_data.update({k: v for k, v in row.items() if k not in PII_FIELDS})
                log_message = '; '.join([f"{key}={value}" for key, value in filtered_data.items()])
                logger.info(f"{log_message};\nFiltered fields:\n{', '.join(PII_FIELDS)}")

        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")

        finally:
            cursor.close()
            db_connection.close()


if __name__ == "__main__":
    main()
