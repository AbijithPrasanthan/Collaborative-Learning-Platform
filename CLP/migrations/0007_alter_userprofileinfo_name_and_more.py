# Generated by Django 4.0.1 on 2022-01-17 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CLP', '0006_userprofileinfo_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='name',
            field=models.CharField(default='default name', max_length=256),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='rollno',
            field=models.CharField(default='1234567891234567', max_length=16),
        ),
    ]