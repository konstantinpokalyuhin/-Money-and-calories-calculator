import datetime as dt

class Calculator:
#Родительский класс.
    def __init__(self, limit):
    #Конструктор.
        self.limit = limit
        self.records = []
        
    def add_record(self, record):
    #Делает новую запись в списке.
        self.records.append(record)

    def get_today_stats(self):
    #Количество потраченных денег за сегодня.
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):
    #Расчет денег и калорий за последние 7 дней.
        today = dt.date.today()
        delta_week = today - dt.timedelta(days=7)
        week = 0
        for i in self.records:
            if delta_week <=  i.date <= today:
                week += i.amount
        return week

    def balance_day(self):
    #Сыитает остаток
        balance_day = self.limit - self.get_today_stats()
        return balance_day


class Record:

    def __init__(self, amount, comment, date = None):
    #Присваивает дату если её нету, преобразовывает строки в дату.
        self.amount = amount
        self.comment = comment 
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date,'%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
#Дочерний класс. Выводит количество калорий.

     def get_calories_remained(self):
        cal_balance_day = self.balance_day()
        if cal_balance_day > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
            f'калорийностью не более {cal_balance_day} кКал')
        else:
            return 'Хватит есть!'


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
        "На сегодня осталось {spent} "
        "{currency_name}"
        )
    DEBT_CASH = (
        "Денег нет, держись: твой долг - "
        "{spent} {currency_name}"
        )
    NO_CASH = ("Денег нет, держись")
    NO_CURRENCY = (
        "Данная валюта {no_currency} не поддерживается"
        )
    
    def get_today_cash_remained(self, currency):
       
        #Обработка исключений.
        if currency not in self.CURRENCIES: 
            raise ValueError(self.NO_CURRENCY.format(
                no_currency=currency
                ))

        balance_day = self.balance_day()
        
        if balance_day == 0:
            return self.NO_CASH
         
        rate, currency_name = self.CURRENCIES[currency]
        spent_by_currency = round(balance_day / rate, 2)
        if balance_day > 0:
            return self.CASH_REMAINS.format(
                spent=spent_by_currency,
                currency_name=currency_name
                )
        else:
            return self.DEBT_CASH.format(
                spent=abs(spent_by_currency),
                currency_name=currency_name
                )

cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
print(cash_calculator.get_today_cash_remained('rub'))                                  