# Generated by Django 3.2.8 on 2022-07-08 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibleapp', '0015_auto_20220708_1429'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Chines_Bible',
            new_name='Chinese_Bible',
        ),
        migrations.RemoveField(
            model_name='daily_bible',
            name='chinses',
        ),
        migrations.RemoveField(
            model_name='daily_bible',
            name='esv',
        ),
    ]
