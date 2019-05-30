# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-28 01:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0134_add_compliance_reporting_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'compliance_report_schedule_c',
            },
        ),
        migrations.CreateModel(
            name='ScheduleCRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='api.ScheduleC')),
            ],
            options={
                'db_table': 'compliance_report_schedule_c_record',
            },
        ),
        migrations.AddField(
            model_name='compliancereport',
            name='schedule_c',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compliance_report', to='api.ScheduleC'),
        ),
    ]