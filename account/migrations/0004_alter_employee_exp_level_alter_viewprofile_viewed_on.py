# Generated by Django 4.2.11 on 2024-04-17 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_rename_profile_viewprofile_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='exp_level',
            field=models.CharField(choices=[('Junior', 'Junior'), ('Mid', 'Mid'), ('Senior', 'Senior')], max_length=6),
        ),
        migrations.AlterField(
            model_name='viewprofile',
            name='viewed_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
