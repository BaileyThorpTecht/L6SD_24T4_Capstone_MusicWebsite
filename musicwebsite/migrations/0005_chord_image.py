# Generated by Django 5.1.2 on 2024-11-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicwebsite', '0004_chord_iscustom'),
    ]

    operations = [
        migrations.AddField(
            model_name='chord',
            name='image',
            field=models.CharField(db_default='', max_length=99999),
        ),
    ]
