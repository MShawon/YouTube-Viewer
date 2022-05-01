"""
MIT License

Copyright (c) 2021-2022 MShawon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import shutil
import sqlite3
from contextlib import closing
from datetime import datetime


def create_database(database, database_backup):
    with closing(sqlite3.connect(database)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS
            statistics (date TEXT, view INTEGER)""")

            connection.commit()

    try:
        os.remove(database_backup)
    except Exception:
        pass

    try:
        shutil.copy(database, database_backup)
    except Exception:
        pass


def update_database(database, threads, increment=1):
    today = str(datetime.today().date())
    with closing(sqlite3.connect(database, timeout=threads*10)) as connection:
        with closing(connection.cursor()) as cursor:
            try:
                cursor.execute(
                    "SELECT view FROM statistics WHERE date = ?", (today,))
                previous_count = cursor.fetchone()[0]
                cursor.execute("UPDATE statistics SET view = ? WHERE date = ?",
                               (previous_count + increment, today))
            except Exception:
                cursor.execute(
                    "INSERT INTO statistics VALUES (?, ?)", (today, 0),)

            connection.commit()
