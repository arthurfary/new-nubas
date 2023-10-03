import datetime
from cogs.currency.currency_db_handler import Database
#from currency_db_handler import Database

class InterestHandler:
    def __init__(self, db_path, last_interest_path='cogs/currency/last_interest.txt', rate=0.001):
        self.db = Database(db_path)
        self.last_interest_path = last_interest_path
        self.rate = rate

    def is_one_day_passed_since_registered_datetime(self):
        now = datetime.datetime.now()
        format = "%Y-%m-%d %H:%M:%S.%f"
        last = self.get_registered_datetime()

        if now > datetime.datetime.strptime(last, format) + datetime.timedelta(days=1):
            return True
        else:
            return False

    def get_registered_datetime(self):
        with open(self.last_interest_path, 'r', encoding='utf-8') as f:
            return f.read()

    def set_registered_datetime(self, date):
        with open(self.last_interest_path, 'w', encoding='utf-8') as f:
            f.write(str(date))

    def update_registered_datetime(self):
        self.set_registered_datetime(datetime.datetime.now())

    def add_intrest_if_one_day_is_passed(self):
        if self.is_one_day_passed_since_registered_datetime():
            self.db.add_intrest_to_all_registered_accounts(self.rate)
            self.update_registered_datetime()

# Uso:
#handler = InterestHandler('cogs/currency/currency.db', 'cogs/currency/last_interest.txt')
#handler.add_intrest_if_one_day_is_passed()
