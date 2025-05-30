# Generated by Django 5.1.2 on 2025-02-21 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='name',
            new_name='username',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
