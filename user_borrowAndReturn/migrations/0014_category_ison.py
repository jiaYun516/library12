# Generated by Django 4.2.5 on 2024-01-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_borrowAndReturn', '0013_book_ison'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='isOn',
            field=models.BooleanField(default=True),
        ),
    ]
