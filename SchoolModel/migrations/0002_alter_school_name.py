# Generated by Django 3.2.1 on 2021-05-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]