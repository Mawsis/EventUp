# Generated by Django 4.1.4 on 2023-02-06 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventUp', '0019_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
    ]
