# Generated by Django 3.2.25 on 2025-05-28 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='cdefault_ounty',
            new_name='default_county',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='tdefault_own_or_city',
            new_name='default_town_or_city',
        ),
    ]
