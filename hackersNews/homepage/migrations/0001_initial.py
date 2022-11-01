# Generated by Django 4.1 on 2022-11-01 18:25

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('karma', models.Field(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('site', models.URLField(max_length=255)),
                ('descendants', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=1)),
                ('votes', models.BooleanField(default=False)),
                ('show_dt', models.BooleanField(default=False)),
                ('ask_dt', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insert_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('votes', models.IntegerField(default=1)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.post')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.user')),
            ],
        ),
    ]
