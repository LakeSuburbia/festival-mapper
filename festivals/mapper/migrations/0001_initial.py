# Generated by Django 4.1.4 on 2022-12-18 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Festival",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("location", models.CharField(max_length=100)),
                ("deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="FestivalArtist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("deleted", models.BooleanField(default=False)),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mapper.artist"
                    ),
                ),
                (
                    "festival",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mapper.festival",
                    ),
                ),
            ],
        ),
    ]
