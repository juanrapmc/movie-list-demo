# Generated by Django 2.1.1 on 2018-09-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movielistapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
