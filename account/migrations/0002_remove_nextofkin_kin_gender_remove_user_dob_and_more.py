# Generated by Django 5.0.1 on 2024-03-20 19:13

import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nextofkin',
            name='kin_gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='user',
            name='doctor_id',
        ),
        migrations.AlterField(
            model_name='appointmentroom',
            name='room_type',
            field=models.CharField(choices=[('', '-----'), ('Consultation', 'Consultation'), ('Reproductive Health', 'Reproductive Health'), ('HIV VCT', 'HIV VCT'), ('Examination', 'Examination room'), ('Intensive Care', 'Intensive Care Unit (ICU)'), ('Dental Unit', 'Dental Unit'), ('Pharmacy', 'Pharmacy'), ('Admission', 'Admission')], max_length=19, verbose_name='Room Type'),
        ),
        migrations.AlterField(
            model_name='nextofkin',
            name='kin_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=13, null=True, region=None, unique=True),
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('otp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('otp_verified', models.BooleanField(default=False)),
                ('for_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
