# Generated by Django 3.2 on 2021-04-20 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20210420_1314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title', 'author'], 'permissions': (('can_modify_books', 'Can add, update and delete books.'),)},
        ),
    ]
