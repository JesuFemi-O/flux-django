# Generated by Django 3.2.7 on 2021-09-15 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='onwer',
            new_name='owner',
        ),
    ]