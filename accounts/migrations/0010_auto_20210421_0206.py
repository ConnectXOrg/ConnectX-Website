# Generated by Django 3.1.6 on 2021-04-21 02:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210307_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(default='default_aze1tf.png', max_length=255, verbose_name='Profile picture'),
        ),
    ]
