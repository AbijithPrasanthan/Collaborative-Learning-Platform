# Generated by Django 4.0.1 on 2022-01-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CLP', '0005_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
