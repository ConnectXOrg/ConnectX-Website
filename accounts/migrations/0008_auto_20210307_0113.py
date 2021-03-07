# Generated by Django 3.1.6 on 2021-03-07 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0009_auto_20210307_0053'),
        ('accounts', '0007_studentprofile_interview_requests'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='acceptances',
            field=models.ManyToManyField(related_name='employer_acceptances', to='marketplace.Listing'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='interview_requests',
            field=models.ManyToManyField(related_name='employer_interview_requests', to='marketplace.Listing'),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='rejections',
            field=models.ManyToManyField(related_name='employer_rejections', to='marketplace.Listing'),
        ),
    ]
