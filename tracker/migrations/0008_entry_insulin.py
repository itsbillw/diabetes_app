# Generated by Django 2.0.5 on 2018-06-03 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_auto_20180603_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='insulin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
