"""OOP Calculator for money and calories"""

import datetime as dt

DATE_FORMAT = '%d.%m.%Y'

class Record():
    """Класс для хранения записей"""
    amount: float
    date: str
    comment: str

    def __init__(self, amount, comment, date=None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = date
        if self.date is None:
            self.date = dt.datetime.now().strftime(DATE_FORMAT)

class Calculator():
    """Класс основного калькулятора"""
    
    limit: float

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []
    
    def add_record(self, record:Record) -> None:
        """Добавляет запись"""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Выводит потраченное значения за сегодня"""
        spend_money_today = float()
        for record in self.records:
            if record.date == dt.datetime.now().strftime(DATE_FORMAT):
                spend_money_today+=record.amount
        return spend_money_today
    
    def get_week_stats(self) -> float:
        """Выводит потраченное значения за неделю"""
        spend_money_week = float()
        date_week_ago = dt.datetime.now().date() - dt.timedelta(days=7)
        for record in self.records:
            if dt.datetime.strptime(record.date, DATE_FORMAT).date() > date_week_ago:
                spend_money_week += record.amount
        return spend_money_week
    
    def get_remaining_value(self) -> float:
        """Считает сколько денег/калорий еще можно потратить сегодня"""
        today_money = self.get_today_stats()
        return self.limit - today_money

class CaloriesCalculator(Calculator):
    """Класс калькулятора калорий"""
    
    NO_CALORIES_RESPONSE = 'Хватит есть!'
    REMAIN_CALORIES_RESPONSE = (
        'Сегодня можно съесть что-нибудь еще, но '
        'с общей калорийностью не более {calories} кКал'
        )

    def get_calories_remained(self) -> str:
        """Считает сколько еще калорий можно съесть и выводит"""
        calories_remained = self.get_remaining_value()
        if calories_remained > 0:
            return self.REMAIN_CALORIES_RESPONSE.format(calories=calories_remained)
        else:
            return self.NO_CALORIES_RESPONSE

class CashCalculator(Calculator):
    """Класс калькулятора денег"""
    
    CURRENSY_RATE ={
        'rub':(1, 'руб'),
        'usd':(80, 'USD'),
        'eur':(100, 'Euro')
    }

    NO_MONEY_RESPONSE = 'Денег нет, держись'
    DEBT_MONEY_RESPONSE = 'Денег нет, держись: твой долг - {value} {valute}'
    REMAIN_MONEY_RESPONSE = 'На сегодня осталось {value} {valute}'

    def get_today_cash_remained(self, currency) -> str:
        """Считает сколько еще денег можно потратить и выводит"""
        money_remained = self.get_remaining_value()
        if money_remained > 0:
            return self.REMAIN_MONEY_RESPONSE.format(value = money_remained / self.CURRENSY_RATE[currency][0], valute = self.CURRENSY_RATE[currency][1])
        if money_remained == 0:
            return self.NO_MONEY_RESPONSE
        if money_remained < 0:
            return self.DEBT_MONEY_RESPONSE.format(value = money_remained / self.CURRENSY_RATE[currency][0], valute = self.CURRENSY_RATE[currency][1])

if __name__ == '__main__':

    cash = CashCalculator(1000)
    
    cash.add_record(Record(amount=100, comment='Обед'))                             # Обед, сегодня, цена - 100
    cash.add_record(Record(amount=150, comment='Подарок Жене', date='03.05.2023'))  # Подарок жене, вчера, цена -150

    print(cash.get_today_stats())   # Потратил сегодня
    print(cash.get_week_stats())    # Потратил за неделю

    print(cash.get_today_cash_remained('rub'))  # Осталось в руб
    print(cash.get_today_cash_remained('usd'))  # Осталось в usd
    print(cash.get_today_cash_remained('eur'))  # Осталось в eur
    
    cash.add_record(Record(amount=900, comment='Такси'))    # Такси, сегодня, цена - 900
    
    print(cash.get_today_cash_remained('rub'))  # Осталось в руб
    print(cash.get_today_cash_remained('usd'))  # Осталось в usd
    print(cash.get_today_cash_remained('eur'))  # Осталось в eur
    
    cash.add_record(Record(amount=5000, comment='Новый телефон'))     # Новый телефон, сегодня, цена - 5000

    print(cash.get_today_cash_remained('rub'))  # Осталось в руб
    print(cash.get_today_cash_remained('usd'))  # Осталось в usd
    print(cash.get_today_cash_remained('eur'))  # Осталось в eur

    print('-'*50)

    calories = CaloriesCalculator(1000)

    calories.add_record(Record(amount=100, comment='Обед'))                        # Обед, сегодня, калорий - 100
    calories.add_record(Record(amount=150, comment='Фастфуд', date='03.05.2023'))  # Фастфуд, вчера, калорий -150
    
    print(calories.get_today_stats())   # Потратил сегодня
    print(calories.get_week_stats())    # Потратил за неделю

    print(calories.get_calories_remained()) #Осталось калорий

    calories.add_record(Record(amount=900, comment='Пироженое'))# Пироженое, сегодня, калорий -900
    print(calories.get_calories_remained()) #Осталось калорий