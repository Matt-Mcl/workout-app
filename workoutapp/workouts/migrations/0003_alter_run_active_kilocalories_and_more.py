# Generated by Django 4.0.2 on 2022-03-03 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0002_alter_run_actual_distance_alter_run_elevation_gain_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='active_kilocalories',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='run',
            name='average_cadence',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='run',
            name='location',
            field=models.CharField(blank=True, choices=[('O', 'Outdoor'), ('I', 'Indoor')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='walk',
            name='active_kilocalories',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='walk',
            name='average_heart_rate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='walk',
            name='location',
            field=models.CharField(blank=True, choices=[('O', 'Outdoor'), ('I', 'Indoor')], max_length=1, null=True),
        ),
    ]
