# Generated by Django 3.1.5 on 2021-02-17 19:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=True, null=True)),
                ('created_date', models.DateTimeField(editable=False)),
                ('updated_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_date', models.DateField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(editable=False)),
                ('updated_date', models.DateTimeField()),
                ('completed', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('enabled', models.BooleanField(default=True, null=True)),
                ('created_date', models.DateTimeField(editable=False)),
                ('updated_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('enabled', models.BooleanField(default=True, null=True)),
                ('created_date', models.DateTimeField(editable=False)),
                ('updated_date', models.DateTimeField()),
                ('spending', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weekly_expenses_spending', to='api.spending')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.FloatField(default=0)),
                ('enabled', models.BooleanField(default=True, null=True)),
                ('created_date', models.DateTimeField(editable=False)),
                ('updated_date', models.DateTimeField()),
                ('period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_period', to='api.period')),
                ('spending', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_spending', to='api.spending')),
                ('weekly_expenses', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weekly_expenses_transaction', to='api.weeklyexpenses')),
            ],
        ),
    ]
