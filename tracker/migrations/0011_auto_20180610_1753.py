# Generated by Django 2.0.5 on 2018-06-10 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0010_auto_20180603_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='event_type',
            field=models.CharField(choices=[('Manual', 'Manual'), ('Dexcom', 'Auto')], default='Manual', max_length=9),
        ),
        migrations.AlterField(
            model_name='entry',
            name='insulin_type',
            field=models.CharField(choices=[('Tresiba', 'Basal'), ('Fiasp', 'Bolus')], default='Fiasp', max_length=9, null=True),
        ),
    ]
