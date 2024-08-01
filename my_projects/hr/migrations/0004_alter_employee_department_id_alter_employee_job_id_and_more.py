# Generated by Django 5.0.6 on 2024-07-14 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_alter_job_salary_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='job_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.job'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee'),
        ),
    ]
