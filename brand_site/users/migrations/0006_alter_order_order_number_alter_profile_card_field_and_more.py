# Generated by Django 4.2.3 on 2023-09-16 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_card_field_profile_tinkoff_pay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(default=405918),
        ),
        migrations.AlterField(
            model_name='profile',
            name='card_field',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tinkoff_pay',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='yandex_pay',
            field=models.BigIntegerField(default=0),
        ),
    ]
