# Generated by Django 3.0.3 on 2020-02-27 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_auto_20200227_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='package_type',
            field=models.CharField(default='', max_length=30),
        ),
    ]