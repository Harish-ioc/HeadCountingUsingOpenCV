# Generated by Django 5.0.1 on 2024-03-27 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportings', '0013_friday_teacher_saturday_teacher_thursday_teacher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friday',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='friday', to='reportings.class'),
        ),
        migrations.AlterField(
            model_name='monday',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='monday', to='reportings.class'),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='saturday', to='reportings.class'),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='thursday', to='reportings.class'),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tuesday', to='reportings.class'),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='class_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wednesday', to='reportings.class'),
        ),
    ]
