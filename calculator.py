"""OOP Calculator for money and calories."""

import datetime as dt
import unittest
from dataclasses import dataclass, field

DATE_FORMAT = '%d.%m.%Y'

@dataclass
class Record():
    """Класс для хранения записей."""
    amount: float
    comment: str
    date: str = None

    if date is None:
        date = dt.datetime.now().strftime(DATE_FORMAT)

@dataclass
class Calculator():
    """Класс основного калькулятора."""
    
    limit: float
    records: list = field(default_factory=list)

    def add_record(self, record:Record) -> None:
        """Добавляет запись."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Выводит потраченное значения за сегодня."""
        return float(sum(record.amount for record in self.records if record.date == dt.datetime.now().strftime(DATE_FORMAT)))
    
    def get_week_stats(self) -> float:
        """Выводит потраченное значения за неделю."""
        date_week_ago = dt.datetime.now().date() - dt.timedelta(days=7)
        return float(sum(record.amount for record in self.records if dt.datetime.strptime(record.date, DATE_FORMAT).date() > date_week_ago))
    
    def get_remaining_value(self) -> float:
        """Считает сколько денег/калорий еще можно потратить сегодня."""
        return self.limit - self.get_today_stats()

class CaloriesCalculator(Calculator):
    """Класс калькулятора калорий."""

    NO_CALORIES_RESPONSE = 'Хватит есть!'
    REMAIN_CALORIES_RESPONSE = (
        'Сегодня можно съесть что-нибудь еще, но '
        'с общей калорийностью не более {calories} кКал'
        )

    def get_calories_remained(self) -> str:
        """Считает сколько еще калорий можно съесть и выводит."""
        calories_remained = self.get_remaining_value()
        if calories_remained > 0:
            return self.REMAIN_CALORIES_RESPONSE.format(calories=calories_remained)
        return self.NO_CALORIES_RESPONSE

class CashCalculator(Calculator):
    """Класс калькулятора денег."""
    
    CURRENSY_RATE ={
        'rub':(1, 'руб'),
        'usd':(80, 'USD'),
        'eur':(100, 'Euro')
    }

    NO_MONEY_RESPONSE = 'Денег нет, держись'
    DEBT_MONEY_RESPONSE = 'Денег нет, держись: твой долг - {value} {valute}'
    REMAIN_MONEY_RESPONSE = 'На сегодня осталось {value} {valute}'

    def get_today_cash_remained(self, currency:str) -> str:
        """Считает сколько еще денег можно потратить и выводит."""
        money_remained = self.get_remaining_value()
        if money_remained > 0:
            return self.REMAIN_MONEY_RESPONSE.format(value = money_remained / self.CURRENSY_RATE[currency][0], valute = self.CURRENSY_RATE[currency][1])
        if money_remained == 0:
            return self.NO_MONEY_RESPONSE
        return self.DEBT_MONEY_RESPONSE.format(value = money_remained / self.CURRENSY_RATE[currency][0], valute = self.CURRENSY_RATE[currency][1])

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.cash = CashCalculator(1000)
        self.cash.add_record(Record(amount=100, comment='Обед'))
        self.cash.add_record(Record(amount=150, comment='Подарок Жене', date='05.05.2023'))
        
        self.calories = CaloriesCalculator(1000)
        self.calories.add_record(Record(amount=50, comment='Обед'))
        self.calories.add_record(Record(amount=300, comment='Фастфуд', date='05.05.2023'))
    
    def test_cash_stats(self):
        self.assertEqual(self.cash.get_today_stats(), 100.0)
        self.assertEqual(self.cash.get_week_stats(), 250.0)
        
    
    def test_calories_stats(self):
        self.assertEqual(self.calories.get_today_stats(), 50.0)
        self.assertEqual(self.calories.get_week_stats(), 350.0)
    
    def test_cash_remained(self):
        self.assertEqual(self.cash.get_today_cash_remained('rub'), 'На сегодня осталось 900.0 руб')
        self.assertEqual(self.cash.get_today_cash_remained('usd'), 'На сегодня осталось 11.25 USD')
        self.assertEqual(self.cash.get_today_cash_remained('eur'), 'На сегодня осталось 9.0 Euro')
        self.assertEqual(self.calories.get_calories_remained(), 'Сегодня можно съесть что-нибудь еще, но с общей калорийностью не более 950.0 кКал')
    
    def test_no_value(self):
        self.cash = CashCalculator(0)
        self.calories = CaloriesCalculator(0)

        self.assertEqual(self.cash.get_today_cash_remained('rub'), 'Денег нет, держись')
        self.assertEqual(self.cash.get_today_cash_remained('usd'), 'Денег нет, держись')
        self.assertEqual(self.cash.get_today_cash_remained('eur'), 'Денег нет, держись')
        self.assertEqual(self.calories.get_calories_remained(), 'Хватит есть!')
    
    def test_cash_debt(self):
        self.cash = CashCalculator(-100)
        self.assertEqual(self.cash.get_today_cash_remained('rub'), 'Денег нет, держись: твой долг - -100.0 руб')
        self.assertEqual(self.cash.get_today_cash_remained('usd'), 'Денег нет, держись: твой долг - -1.25 USD')
        self.assertEqual(self.cash.get_today_cash_remained('eur'), 'Денег нет, держись: твой долг - -1.0 Euro')

if __name__ == '__main__':
    unittest.main()