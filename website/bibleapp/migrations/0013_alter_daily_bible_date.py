# Generated by Django 3.2.8 on 2022-07-07 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibleapp', '0012_daily_bible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_bible',
            name='Date',
            field=models.CharField(max_length=50),
        ),
    ]
