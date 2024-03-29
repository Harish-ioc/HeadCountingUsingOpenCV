# Generated by Django 5.0.1 on 2024-01-31 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Snaps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_hour', models.IntegerField()),
                ('max_hour', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=100)),
                ('usr', models.CharField(max_length=200)),
                ('pwd', models.CharField(max_length=200)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to='process.block')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('period', models.CharField(max_length=50)),
                ('count', models.IntegerField()),
                ('cam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='process.camera')),
            ],
        ),
        migrations.CreateModel(
            name='Seconds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second', models.IntegerField()),
                ('snap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second', to='process.snaps')),
            ],
        ),
        migrations.CreateModel(
            name='Minutes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.IntegerField()),
                ('snap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minutes', to='process.snaps')),
            ],
        ),
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=10)),
                ('hour', models.IntegerField()),
                ('snap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeperiod', to='process.snaps')),
            ],
        ),
    ]
