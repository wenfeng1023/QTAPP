# Generated by Django 3.2.8 on 2022-07-20 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibleapp', '0019_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='profiel_ima',
            field=models.ImageField(blank=True, default='img/user.png', null=True, upload_to='img'),
        ),
    ]
