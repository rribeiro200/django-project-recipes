# Generated by Django 5.0.1 on 2024-01-26 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_author_alter_recipe_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
