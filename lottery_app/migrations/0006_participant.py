# Generated by Django 5.1.4 on 2025-05-01 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery_app', '0005_lottery_is_deployed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('participant_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('mobile_number', models.CharField(max_length=15)),
                ('wallet_address', models.CharField(max_length=42)),
                ('is_winner', models.BooleanField(default=False)),
                ('wining_amount', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('lottery_number', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lottery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lottery_app.lottery')),
            ],
        ),
    ]
