# Generated by Django 5.0.1 on 2024-03-26 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_remove_appointment_appointed_room_and_more'),
        ('payments', '0009_remove_payment_appoint_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='account.appointment'),
        ),
    ]
