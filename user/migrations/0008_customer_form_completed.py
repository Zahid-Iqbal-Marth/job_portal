# Generated by Django 3.0.3 on 2020-03-01 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200301_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='form_completed',
            field=models.BooleanField(default=False),
        ),
    ]
