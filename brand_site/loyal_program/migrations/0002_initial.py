# Generated by Django 4.2.3 on 2024-02-20 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('loyal_program', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='profile',
            field=models.ManyToManyField(related_name='promocode', to='users.profile'),
        ),
    ]
