# Generated by Django 4.2.1 on 2023-07-24 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elevator',
            old_name='available',
            new_name='is_available',
        ),
    ]
