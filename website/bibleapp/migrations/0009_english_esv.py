# Generated by Django 3.2.8 on 2022-07-06 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibleapp', '0008_greek_bible'),
    ]

    operations = [
        migrations.CreateModel(
            name='English_ESV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Book', models.CharField(max_length=100)),
                ('Book_No', models.CharField(max_length=100)),
                ('Chapter', models.CharField(max_length=100)),
                ('Verse', models.CharField(max_length=100)),
                ('Text', models.TextField()),
            ],
        ),
    ]
