import hashlib
import uuid
from pprint import pprint
from urllib.parse import urlencode


class PaymentMethod:
    """ Платежные методы """

    PAY = 'pay/'  # пополние
    ...


class Currency:
    """ Валюты """

    RU = "RUB"
    ...


class AAIOBank:
    BASE_URL = "https://aaio.so/merchant/"

    def __init__(self,
                 merchant_id: str,
                 aaio_api_key: str) -> None:
        self.sign = None
        self.amount = None
        self.currency = None
        self.order_id = None
        self.desc = None
        self.lang = None
        self.merchant_id: str = merchant_id
        self.aaio_api_key: str = aaio_api_key

    def generate_payment_information(self, amount: float):
        self.amount = amount
        self.currency = Currency.RU
        self.order_id = uuid.uuid4()
        self.desc = 'Order Payment'
        self.lang = 'ru'

    def generate_signature(self):
        self.sign = f':'.join([
            str(self.merchant_id),
            str(self.amount),
            str(self.currency),
            str(self.aaio_api_key),
            str(self.order_id)
        ])

    def create_payment(self, amount: float):
        self.generate_payment_information(amount)
        self.generate_signature()

        if not self.sign:
            raise ValueError("Not sing yet")

        params = {
            'merchant_id': self.merchant_id,
            'amount': self.amount,
            'currency': self.currency,
            'order_id': self.order_id,
            'sign': hashlib.sha256(self.sign.encode('utf-8')).hexdigest(),
            'desc': self.desc,
            'lang': self.lang
        }

        url_encode = urlencode(params)
        payment_data = {
            'amount': self.amount,
            'url': self.BASE_URL + PaymentMethod.PAY + '?' + url_encode,
            'order_id': self.order_id
        }

        return payment_data


AAIO_API_KEY = 'NWJkMTgwY2UtYWU3ZS00NTE1LTkyYTAtZWQyMmU1MjdlOTQwOmFZV1d3X0EpX0lZX2RTKmU2VitYd0pnK2FsaWRNME5k'

bank = AAIOBank(aaio_api_key=AAIO_API_KEY, merchant_id='')

url = bank.create_payment(100)
pprint(url)
