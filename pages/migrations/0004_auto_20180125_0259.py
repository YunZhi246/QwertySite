# Generated by Django 2.0.1 on 2018-01-25 07:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20180125_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date'),
        ),
    ]
