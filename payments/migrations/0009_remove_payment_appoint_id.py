# Generated by Django 5.0.1 on 2024-03-25 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_rename_appointment_id_payment_appoint_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='appoint_id',
        ),
    ]
