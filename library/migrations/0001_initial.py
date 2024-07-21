# Generated by Django 5.0.7 on 2024-07-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bName', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=20)),
                ('published', models.DateField()),
            ],
        ),
    ]
