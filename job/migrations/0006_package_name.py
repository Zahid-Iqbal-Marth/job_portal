# Generated by Django 3.0.3 on 2020-02-27 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_package_job_posted_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='name',
            field=models.TextField(default='', max_length=30),
        ),
    ]