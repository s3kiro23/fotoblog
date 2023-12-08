# Generated by Django 4.1.7 on 2023-03-19 19:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_follows_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'CREATOR'}, null=True, to=settings.AUTH_USER_MODEL, verbose_name='suit'),
        ),
    ]