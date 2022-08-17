# Generated by Django 3.2.8 on 2022-08-03 02:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bibleapp', '0022_rename_profiel_img_user_profile_profile_img'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_profile',
            options={'verbose_name': 'user_profile', 'verbose_name_plural': 'user_profile'},
        ),
        migrations.CreateModel(
            name='My_Meditation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public', models.BooleanField(default=False)),
                ('private', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Meditation',
                'ordering': ('-created_date',),
            },
        ),
    ]
