# Generated by Django 3.2 on 2021-04-19 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20210418_1815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Can set book as returned'), ('can_renew', 'Can set book as renewed'))},
        ),
    ]