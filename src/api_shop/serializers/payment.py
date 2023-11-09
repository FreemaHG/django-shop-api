from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    """
    Схема для входных данных при оплате заказа
    """

    number = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=100)
    month = serializers.CharField(max_length=2)
    year = serializers.CharField(max_length=4)
    code = serializers.CharField(max_length=3)

    def validate_number(self, value: str):
        """
        Проверка, что введены цифры
        """
        if not value.isdigit():
            raise serializers.ValidationError("Введен некорректный номер карты")
        return value

    def validate_month(self, value: str):
        """
        Проверка корректности номера месяца
        """
        if not value.isdigit() or int(value) > 12 or int(value) < 1:
            raise serializers.ValidationError("Номер месяца введен некорректно")
        return value

    def validate_year(self, value: str):
        """
        Проверка корректности введенного года
        """
        if not value.isdigit() or int(value) > 3000 or int(value) < 2000:
            raise serializers.ValidationError("Введен некорректный год")
        return value

    def validate_code(self, value: str):
        """
        Проверка корректности введенного кода
        """
        if not value.isdigit():
            raise serializers.ValidationError("Введен некорректный код")
        return value

    class Meta:
        fields = "__all__"
