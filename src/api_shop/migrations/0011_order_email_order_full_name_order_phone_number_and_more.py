# Generated by Django 4.2.5 on 2023-11-06 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_shop', '0010_alter_order_address_alter_order_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=150, null=True, verbose_name='ФИО'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=10, null=True, verbose_name='телефон'),
        ),
        migrations.AlterField(
            model_name='order',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата оформления'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Оформление'), (2, 'Оформлен'), (3, 'Не оплачен'), (4, 'Подтверждение оплаты'), (5, 'Оплачен'), (6, 'Доставляется')], default=1, verbose_name='cтатус'),
        ),
    ]
