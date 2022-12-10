# Generated by Django 4.1.4 on 2022-12-10 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calories_tracker', '0030_elaborations_automatic_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.BinaryField()),
                ('size', models.IntegerField()),
                ('thumbnail', models.BinaryField()),
                ('mime', models.TextField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'files',
                'managed': True,
            },
        ),
    ]
