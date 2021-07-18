import datetime as dt


class Calculator:

    def __init__(self, limit):

        self.limit = limit
        self.records = []

    def add_record(self, record):

        self.records.append(record)

    def get_today_stats(self):

        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):

        today = dt.date.today()
        delta_week = today - dt.timedelta(days=7)
        week = 0
        for i in self.records:
            if delta_week <= i.date <= today:
                week += i.amount
        return week

    def get_remainder(self):

        get_remainder = self.limit - self.get_today_stats()
        return get_remainder


class Record:

    def __init__(self, amount, comment, date=None):

        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):

    EAT_TODAY = (
        'Сегодня можно съесть что-нибудь ещё, но с общей '
        'калорийностью не более {value} кКал')

    STOP_EAT = ('Хватит есть!')

    def get_calories_remained(self):

        cal_balance_day = self.get_remainder()
        if cal_balance_day > 0:
            message = (
                self.EAT_TODAY.format(value=cal_balance_day))
        else:
            message = (self.STOP_EAT)
        return message


class CashCalculator(Calculator):

    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0

    CURRENCIES = {
        'rub': (RUB_RATE, 'руб'),
        'usd': (USD_RATE, 'USD'),
        'eur': (EURO_RATE, 'Euro')
    }
    CASH_REMAINS = (
        'На сегодня осталось {spent} '
        '{currency_name}')
    DEBT_CASH = (
        'Денег нет, держись: твой долг - '
        '{spent} {currency_name}')
    NO_CASH = ('Денег нет, держись')
    NO_CURRENCY = (
        'Данная валюта {no_currency} не поддерживается')

    def get_today_cash_remained(self, currency):

        if currency not in self.CURRENCIES:
            raise ValueError(self.NO_CURRENCY.format(
                no_currency=currency))

        get_remainder = self.get_remainder()

        if get_remainder == 0:
            return self.NO_CASH

        rate, currency_name = self.CURRENCIES[currency]
        spent_by_currency = round(get_remainder / rate, 2)
        if get_remainder > 0:
            return self.CASH_REMAINS.format(
                spent=spent_by_currency,
                currency_name=currency_name)
        else:
            return self.DEBT_CASH.format(
                spent=abs(spent_by_currency),
                currency_name=currency_name)
