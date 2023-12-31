# Generated by Django 4.2.5 on 2023-11-05 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api_shop", "0006_basket"),
    ]

    operations = [
        migrations.AddField(
            model_name="basket",
            name="count",
            field=models.PositiveIntegerField(default=1, verbose_name="кол-во"),
        ),
        migrations.AlterField(
            model_name="basket",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api_shop.product",
                verbose_name="товар",
            ),
        ),
        migrations.AlterField(
            model_name="basket",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="покупатель",
            ),
        ),
    ]
