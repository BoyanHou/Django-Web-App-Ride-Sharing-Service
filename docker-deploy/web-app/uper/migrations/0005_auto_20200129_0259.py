# Generated by Django 3.0.2 on 2020-01-29 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uper', '0004_auto_20200129_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='can_share',
            field=models.CharField(max_length=10),
        ),
    ]
