# Generated by Django 4.2.5 on 2023-11-29 13:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_borrowAndReturn', '0007_book_content_book_publication_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowingrecord',
            name='member',
        ),
        migrations.AddField(
            model_name='borrowingrecord',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='borrowingrecord',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 28, 13, 5, 31, 628187, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
