#!/usr/bin/python
# coding=utf-8

import pymysql
import sys
import logging


class Database:
    """Database connection class."""

    def __init__(self, host, username, password, port, dbname):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.dbname = dbname
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.username,
                    passwd=self.password,
                    db=self.dbname,
                    connect_timeout=5
                )
        except pymysql.MySQLError as e:
            logging.error(e)
            sys.exit()
            # pass
        finally:
            # logging.info('Connection opened successfully.')
            pass

    def run_query(self, query):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                if ('select' or 'SELECT') in query:
                    records = []
                    cur.execute(query)
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                    cur.close()
                    return records
                result = cur.execute(query)
                self.conn.commit()
                affected = f"{cur.rowcount} rows affected."
                cur.close()
                return affected
        except pymysql.MySQLError as e:
            logging.error(e)
            sys.exit()
            # pass
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                # logging.info('Database connection closed.')       