# Generated by Django 3.1.6 on 2021-02-16 19:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0003_auto_20210215_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='saves',
            field=models.ManyToManyField(blank=True, related_name='saves', to=settings.AUTH_USER_MODEL),
        ),
    ]