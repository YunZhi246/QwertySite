# Generated by Django 2.0.1 on 2018-01-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0005_auto_20180115_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Current', 'Current'), ('Hiatus', 'Hiatus'), ('Dropped', 'Dropped'), ('Future', 'Future')], default='Current', max_length=10),
        ),
    ]
