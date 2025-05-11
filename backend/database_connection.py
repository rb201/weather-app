import os
import sqlite3

from contextlib import contextmanager


class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = None

        try:
            CWD = os.path.dirname(os.path.abspath(__file__))
            DATABASE = os.path.join(CWD, self.db_path)

            conn = sqlite3.connect(DATABASE)
            yield conn
        except sqlite3.Error as sqle:
            print(sqle)
            # raise
        finally:
            if conn:
                try:
                    conn.close()
                except sqlite3.Error as sqle:
                    print(f"Error closing sql connection: {sqle}")
