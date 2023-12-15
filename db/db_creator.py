import sqlite3

with sqlite3.connect('db/database.db') as db:
    cursor = db.cursor()
    query = '''CREATE TABLE "IDEAS" (
        "ID"	INTEGER UNIQUE,
        "NAME"	TEXT,
        "RATING"	INT NOT NULL,
        "DESCRIPTION"	TEXT,
        "SUMMARY"	TEXT,
        "THEME"	TEXT,
        "LANGUAGE"	TEXT,
        "LEVEL"	INT,
        "TECHNOLOGIES"	TEXT,
        PRIMARY KEY("ID")
    );'''
    cursor.execute(query)
