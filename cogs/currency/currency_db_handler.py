import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_db_if_not_created()

    def create_db_if_not_created(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY,
            account INTEGER NOT NULL,
            name TEXT NOT NULL,
            money FLOAT NOT NULL);''')
        conn.close()

    def open_connection(self):
        self.conn = sqlite3.connect(self.db_name)

    def close_connection(self):
        self.conn.close()
        def wrapper(self, *args, **kwargs):
            self.open_connection()
            result = function(self, *args, **kwargs)
            self.close_connection()
            return result
        return wrapper

    def commit(self):
        self.conn.commit()

    def query(self, query, params=()):
        cursor = self.conn.execute(query, params)
        return cursor
    
    def fetch_whole_database(self):
        self.open_connection()
        cursor = self.conn.execute("SELECT * from users")
        result = cursor.fetchall()
        self.close_connection()
        return result
    
    def fetch_one_by_uid(self, uid):
        self.open_connection()
        cursor = self.conn.execute("SELECT * from users WHERE id=?", (uid,))
        result = cursor.fetchone()
        self.close_connection()
        return result

    def fetch_one_by_account_num(self, account_number):
        self.open_connection()
        cursor = self.conn.execute("SELECT * from users WHERE account=?", (account_number,))
        result = cursor.fetchone()
        self.close_connection()
        return result

    def create_and_commit_db_entry(self, uid, account_number, name, money=0):
        self.open_connection()
        cursor = self.conn.execute("INSERT INTO users (id, account, name, money) VALUES (?, ?, ?, ?)", (uid, account_number, name, money))
        self.commit()
        self.close_connection()
        return cursor
    
    def add_intrest_to_all_registered_accounts(self, rate):
        self.open_connection()
        cursor = self.conn.execute(f"UPDATE users SET money = money + money * {rate}")
        self.commit()
        self.close_connection()
        return cursor
    
    def fetch_money_by_uid(self, uid):
        self.open_connection()
        cursor = self.conn.execute("SELECT money FROM users WHERE id=?", (uid,))
        result = cursor.fetchone()
        self.close_connection()
        return result[0]
    
    def fetch_money_by_account_number(self, account_number):
        self.open_connection()
        cursor = self.conn.execute("SELECT money FROM users WHERE account=?", (account_number,))
        result = cursor.fetchone()
        self.close_connection()
        return result[0]

    def transfer_money(self, uid, account_number, amount):
        self.open_connection()
        self.conn.execute(f'UPDATE users SET money = money - {amount} WHERE id = ?', (uid,))
        self.conn.execute(f'UPDATE users SET money = money + {amount} WHERE account = ?', (account_number,))
        self.commit()
        self.close_connection()
    

    def fetch_all_accounts(self):
        self.open_connection()
        cursor = self.conn.execute("SELECT account from users")
        result = cursor.fetchall()
        result = [account[0] for account in result]
        self.close_connection()
        return result
    
    def fetch_all_names(self):
        self.open_connection()
        cursor = self.conn.execute("SELECT name from users")
        result = cursor.fetchall()
        result = [name[0] for name in result]
        self.close_connection()
        return result
    
    def add_money_in_account(self, amount, account_number):
        self.open_connection()
        self.conn.execute(f"UPDATE users SET money = money + {amount} WHERE account = ?", (account_number,))
        self.conn.commit()
        self.close_connection()
        

    


