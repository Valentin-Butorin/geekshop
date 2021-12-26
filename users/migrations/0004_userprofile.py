# Generated by Django 3.2.8 on 2021-12-26 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(blank=True, max_length=128, null=True)),
                ('about_me', models.CharField(blank=True, max_length=512, null=True)),
                ('gender', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('U', 'Не указан')], default='U', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
