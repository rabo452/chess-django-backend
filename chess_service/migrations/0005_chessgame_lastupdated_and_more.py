# Generated by Django 5.0.4 on 2024-04-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_service', '0004_gameroom_delete_gamesetup'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessgame',
            name='lastUpdated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='chessgame',
            name='player1SecondsTime',
            field=models.IntegerField(default=2400),
        ),
        migrations.AlterField(
            model_name='chessgame',
            name='player2SecondsTime',
            field=models.IntegerField(default=2400),
        ),
    ]
