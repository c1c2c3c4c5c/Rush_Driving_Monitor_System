# Generated by Django 4.2.4 on 2023-11-05 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0007_remove_driver_latitude_remove_driver_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackernode',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tracker.organization'),
        ),
        migrations.AlterField(
            model_name='trackernode',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tracker.vehicle'),
        ),
    ]
