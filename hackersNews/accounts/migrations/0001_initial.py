# Generated by Django 4.1 on 2022-11-07 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HNUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=255, unique=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email address"
                    ),
                ),
                ("karma", models.IntegerField(default=0)),
                ("date_joined", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
