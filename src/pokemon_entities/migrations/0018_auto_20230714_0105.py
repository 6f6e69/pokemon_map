# Generated by Django 3.1.14 on 2023-07-13 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0017_auto_20230714_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_ent', to='pokemon_entities.pokemon', verbose_name='покемон'),
        ),
    ]
