# Generated by Django 2.0.1 on 2018-01-26 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0010_chapter_displayed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='displayed',
            new_name='visible',
        ),
    ]