# Generated by Django 3.2.12 on 2022-03-25 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medialogue', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='file',
            new_name='src',
        ),
    ]
