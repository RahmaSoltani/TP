# Generated by Django 4.2.4 on 2023-12-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_author_institution_keyword_reference_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='treated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='favoris',
            field=models.ManyToManyField(default=None, to='myapp.article'),
        ),
    ]
