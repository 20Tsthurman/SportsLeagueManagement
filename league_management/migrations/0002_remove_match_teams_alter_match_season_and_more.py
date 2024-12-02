# Generated by Django 5.1.3 on 2024-12-02 22:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='teams',
        ),
        migrations.AlterField(
            model_name='match',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_management.season'),
        ),
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled', max_length=20),
        ),
    ]
