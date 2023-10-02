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

    def handle_connection(function):
        def wrapper(self, *args, **kwargs):
            self.open_connection()
            result = function(self, *args, **kwargs)
            self.commit()
            self.close_connection()
            return result
        return wrapper


    def open_connection(self):
        self.conn = sqlite3.connect(self.db_name)

    def close_connection(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def query(self, query, params=()):
        cursor = self.conn.execute(query, params)
        return cursor
    

    @handle_connection
    def fetch_whole_database(self):
        cursor = self.conn.execute("SELECT * from users")
        return cursor.fetchall()
    

    @handle_connection 
    def fetch_one_by_uid(self, uid):
        cursor = self.conn.execute("SELECT * from users WHERE id=?", (uid,))
        return cursor.fetchone()


    @handle_connection
    def fetch_one_by_account_num(self, account_number):
        cursor = self.conn.execute("SELECT * from users WHERE account=?", (account_number,))
        return cursor.fetchone()


    @handle_connection
    def create_and_commit_db_entry(self, uid, account_number, name, money=0):
        cursor = self.conn.execute("INSERT INTO users (id, account, name, money) VALUES (?, ?, ?, ?)", (uid, account_number, name, money))
        return cursor


    @handle_connection
    def add_intrest_to_all_registered_accounts(self, rate):
        cursor = self.conn.execute(f"UPDATE users SET money = money + money * {rate}")
        return cursor


    @handle_connection
    def fetch_money_by_uid(self, uid):
        cursor = self.conn.execute("SELECT money FROM users WHERE id=?", (uid,))
        return cursor.fetchone()[0]


    @handle_connection
    def fetch_money_by_account_number(self, account_number):
        cursor = self.conn.execute("SELECT money FROM users WHERE account=?", (account_number,))
        return cursor.fetchone()[0]


    @handle_connection
    def transfer_money(self, uid, account_number, amount) -> None:
        self.conn.execute(f'UPDATE users SET money = money - {amount} WHERE id = ?', (uid,))
        self.conn.execute(f'UPDATE users SET money = money + {amount} WHERE account = ?', (account_number,))


    @handle_connection
    def fetch_all_accounts(self) -> list:
        cursor = self.conn.execute("SELECT account from users")
        result = cursor.fetchall()
        return [account[0] for account in result]


    @handle_connection
    def fetch_all_names(self) -> list:
        cursor = self.conn.execute("SELECT name from users")
        result = cursor.fetchall()
        return [name[0] for name in result]


    @handle_connection
    def add_money_in_account(self, amount, account_number):
        self.conn.execute(f"UPDATE users SET money = money + {amount} WHERE account = ?", (account_number,))

