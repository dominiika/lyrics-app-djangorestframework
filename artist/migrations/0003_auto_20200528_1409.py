# Generated by Django 3.0.2 on 2020-05-28 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0002_artist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
