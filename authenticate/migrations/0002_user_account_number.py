# Generated by Django 4.1.3 on 2023-08-01 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
