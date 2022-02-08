import re
from bs4 import BeautifulSoup
import requests
import time

class Currency:

    Bitcoin_Dollar = 'https://www.google.com/finance/quote/BTC-USD?sa=X&ved=2ahUKEwiA2rHEtbT1AhU98rsIHR4UALwQ' \
                     '-fUHegQIAhAS '

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36'}

    current_converted_price = 0
    difference = 1  # Разница после которой будет отправлено сообщение на почту

    def __init__(self):
        price = self.get_currency_price().replace(",", ".")
        price = re.sub(r'\.\d{1,}\d$', '', price)
        self.current_converted_price = float(price)

    def get_currency_price(self):
        response = requests.get(self.Bitcoin_Dollar).text
        soup = BeautifulSoup(response, 'lxml')
        convert = soup.find('div', class_="YMlKec fxKbKc")
        convert = re.sub(r'\.\d{1,}\d$', '', convert.text)
        return convert

    def check_currency(self):
        self.send_massage()
        # currency = float(self.get_currency_price().replace(",", "."))
        # if currency >= self.current_converted_price + self.difference:
        #     print("Курс сильно вырос, может пора что-то делать?")
        #     self.send_massage()
        # elif currency <= self.current_converted_price - self.difference:
        #     print("Курс сильно упал, может пора что-то делать?")
        #     self.send_massage()
        #
        # print("Сейчас курс: 1 битка = " + str(currency))
        time.sleep(3)  # Засыпание программы на 3 секунды
        self.check_currency()

    # Отправка почты через SMTP
    def send_massage(self):
        print('hey go buy eth')