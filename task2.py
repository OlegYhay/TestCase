import datetime
import time

from binance.um_futures import UMFutures
from matplotlib.ticker import FormatStrFormatter

from TokensApi import Api_Key, Secret_Key
import matplotlib.pyplot as plt
import matplotlib.dates

# Api binance
um_client = UMFutures(key=Api_Key, secret=Secret_Key)

# Временной период графика в секундах
TIME_PERIOD = 1
plt.ion()


class Timeline:
    def __init__(self, ticket, time_period) -> None:
        # тикет для которого мы получаем цену
        self.ticket = ticket
        # Временной период обновления
        self.time_period = time_period
        # данные для массива
        self.time_point = []
        self.price_point = []
        # Инициализация пустого графика
        plt.plot([], [])
        # параметры для отслеживания роста за час
        self.start_time = None
        self.start_price = None

    # Получение данных о цене
    def get_price(self) -> None:
        # Получаем цену на указнный тикет
        result = um_client.ticker_price(self.ticket)
        date_current = datetime.datetime.now()

        # Добавляем цену и время для массива данных графика
        self.time_point.append(date_current)
        self.price_point.append(float(result['price']))

        # Начинаем отсчет часа для отслеживания роста на 1%
        if self.start_time == None:
            self.start_time = date_current
            self.start_price = float(result['price'])
        else:
            # расчитываем разницу цены в процентах
            percent = ((float(result['price']) - self.start_price) / self.start_price) * 100
            # Если цена выросла на 1 % тогда выводим сообщение в консоль и устанавливаем новый часовой максимум
            if percent >= 1:
                print(f'Цена выросла на {percent}% с {self.start_price} до {result["price"]}')
                self.start_time = date_current
                self.start_price = float(result['price'])

            # Проверяем не закончился ли час, если да -  устанавливаем новое часовое значение
            date_inf = (date_current - self.start_time).seconds
            if date_inf > 3600:
                self.start_time = date_current
                self.start_price = float(result['price'])

    # Обновление  и вывод графика
    def get_timeline(self) -> None:
        while True:
            self.get_price()
            plt.plot(self.time_point, self.price_point)
            # add title and axis labels
            plt.gcf().autofmt_xdate()
            xfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
            plt.gca().xaxis.set_major_formatter(xfmt)
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.draw()
            plt.gcf().canvas.flush_events()
            time.sleep(self.time_period)
        plt.ioff()
        plt.show()


object_eth = Timeline('ETHUSDT', TIME_PERIOD)
object_eth.get_timeline()
