# Generated by Django 5.0.6 on 2024-07-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_alter_attendence_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='check_out_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
