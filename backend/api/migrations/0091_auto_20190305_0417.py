# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-05 04:17
from __future__ import unicode_literals

import db_comments.model_mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_fuel_code_status_set_effective_dates'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedFuel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_approvedfuel_CREATE_USER', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_approvedfuel_UPDATE_USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'approved_fuel',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.CreateModel(
            name='FeedstockTransportMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_feedstocktransportmode_CREATE_USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'feedstock_transport_mode_fuel_code',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.CreateModel(
            name='FuelTransportMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_fueltransportmode_CREATE_USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fuel_transport_mode_fuel_code',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.CreateModel(
            name='TransportMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_transportmode_CREATE_USER', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_transportmode_UPDATE_USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fuel_transport_mode',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.RemoveField(
            model_name='fuelcode',
            name='feedstock_transport_mode',
        ),
        migrations.AlterField(
            model_name='fuelcode',
            name='fuel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.ApprovedFuel'),
        ),
        migrations.RemoveField(
            model_name='fuelcode',
            name='fuel_transport_mode',
        ),
        migrations.AddField(
            model_name='fueltransportmode',
            name='fuel_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.FuelCode'),
        ),
        migrations.AddField(
            model_name='fueltransportmode',
            name='transport_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.TransportMode'),
        ),
        migrations.AddField(
            model_name='fueltransportmode',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_fueltransportmode_UPDATE_USER', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedstocktransportmode',
            name='fuel_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.FuelCode'),
        ),
        migrations.AddField(
            model_name='feedstocktransportmode',
            name='transport_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.TransportMode'),
        ),
        migrations.AddField(
            model_name='feedstocktransportmode',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_feedstocktransportmode_UPDATE_USER', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fuelcode',
            name='feedstock_transport_mode',
            field=models.ManyToManyField(related_name='_fuelcode_feedstock_transport_mode_+', through='api.FeedstockTransportMode', to='api.TransportMode'),
        ),
        migrations.AddField(
            model_name='fuelcode',
            name='fuel_transport_mode',
            field=models.ManyToManyField(related_name='_fuelcode_fuel_transport_mode_+', through='api.FuelTransportMode', to='api.TransportMode'),
        ),
    ]