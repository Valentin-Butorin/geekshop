# Generated by Django 3.2.8 on 2022-01-14 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('DN', 'завершено'), ('PD', 'оплачено'), ('STP', 'отправлено в обработку'), ('CNL', 'отменено'), ('FM', 'формируется'), ('PRD', 'обработано')], default='FM', max_length=3),
        ),
    ]
