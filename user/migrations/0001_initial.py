# Generated by Django 3.0.2 on 2020-02-22 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession_title', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='profile_pics')),
                ('resume_content', models.CharField(max_length=500)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(max_length=100)),
                ('job_title', models.CharField(max_length=50)),
                ('start_end_date', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=300)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Resume')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=100)),
                ('qualifications', models.CharField(max_length=100)),
                ('start_end_date', models.CharField(max_length=100)),
                ('notes', models.CharField(max_length=300)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Resume')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('EM', 'Employer'), ('CN', 'Candidate')], default='EM', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]