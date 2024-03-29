# Generated by Django 4.2.11 on 2024-03-18 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='elevation_gain',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='flights_climbed',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='swim_cadence',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='total_kilocalories',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='total_swimming_stroke_count',
        ),
        migrations.AddField(
            model_name='workout',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workout',
            name='mins_at_hr',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
