# Generated by Django 4.1.4 on 2022-12-10 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calories_tracker', '0031_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeslinks',
            name='files',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='calories_tracker.files'),
        ),
    ]
