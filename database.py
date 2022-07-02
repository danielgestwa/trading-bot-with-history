#!/usr/bin/python
import sqlite3

class Database:
    def __init__(self):
        self.db = 'stock.db'

        self.create_database('''orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            margin_type text, 
            price real,
            buy real, 
            sell real, 
            stop_loose real, 
            cancel real,
            cancel_time text,
            gain real,
            loose real,
            gain_loose_div real,
            state integer
        )''')
        self.create_database('''transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action text,
            order_id integer,
            margin_type text,
            price real,
            date text
        )''')
        self.create_database('''users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email text UNIQUE
        )''')

    def db_open(self):
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()

    def db_close(self):
        self.con.close()

    def db_execute_data(self, sql, values = []):
        self.cur.execute(sql, values)
        self.con.commit()

    def db_get_data(self, sql, values = []):
        self.cur.execute(sql, values)
        return self.cur.fetchall()

    def create_database(self, db_structure):
        self.db_open()
        self.cur.execute('CREATE TABLE IF NOT EXISTS ' + db_structure)
        self.con.commit()
        self.db_close()