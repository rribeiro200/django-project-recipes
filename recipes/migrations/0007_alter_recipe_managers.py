# Generated by Django 5.0.1 on 2024-02-09 17:02

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_recipe_slug'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='recipe',
            managers=[
                ('my_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
