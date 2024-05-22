from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from src.models import Customer


class GetProfile:
    def __init__(
            self,
            phone_number: str,
            telegram_id: str | int,
            username: str,
            user_keyword: str
    ):
        self.phone_number = phone_number
        self.username = username
        self.telegram_id = telegram_id
        self.user_keyword = user_keyword

    def _get_customer_from_db(self) -> None:
        """
        Получение клиента из базы данных
        """
        self.customer = Customer.objects.filter(phone=self.phone_number).first()
        if not self.customer:
            raise ValidationError({
                "message": "Такого клиента нет в системе"
            })

    def _check_user_keyword(self):
        if self.customer.user_keyword != self.user_keyword:
            raise ValidationError(
                {
                    'message': "Вы неправильно указали слово пароля",
                    'success': False,
                    'data': []
                }, code=400
            )

    def _fill_telegram_user_data(self) -> None:
        """
        Заполнение данных
        """
        self.customer.username = self.username
        self.customer.telegram_id = self.telegram_id
        self.customer.save()

    def execute(self):
        self._get_customer_from_db()
        self._check_user_keyword()
        self._fill_telegram_user_data()

        return Response(
            {
                'message': "Вы успешно авторизовались\nВы будете получать уведомления о брони",
                'success': True,
            }
        )
