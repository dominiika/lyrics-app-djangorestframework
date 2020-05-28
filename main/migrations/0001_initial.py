# Generated by Django 3.0.2 on 2020-05-03 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyAPIToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('expires', models.DateTimeField(blank=True)),
                ('token_did_expire', models.BooleanField()),
            ],
        ),
    ]
