# Generated by Django 4.2.13 on 2024-06-24 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0002_rename_bookingtable_tablebooking_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tableinfo',
            name='availability',
        ),
    ]