# Generated by Django 4.2.5 on 2023-11-29 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_borrowAndReturn', '0010_alter_borrowingrecord_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowingrecord',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 28, 13, 56, 3, 928178, tzinfo=datetime.timezone.utc)),
        ),
    ]
