# Generated by Django 3.0.2 on 2020-02-19 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='dateentered',
            field=models.DateField(blank=True, null=True),
        ),
    ]