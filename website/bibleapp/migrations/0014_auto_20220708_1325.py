# Generated by Django 3.2.8 on 2022-07-08 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bibleapp', '0013_alter_daily_bible_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='english_esv',
            name='tables',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibleapp.daily_bible', verbose_name='tables'),
        ),
        migrations.AddField(
            model_name='korean_bible_c',
            name='tables',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bibleapp.daily_bible', verbose_name='tables'),
        ),
    ]
