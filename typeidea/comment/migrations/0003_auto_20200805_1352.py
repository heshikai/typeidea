# Generated by Django 3.0.8 on 2020-08-05 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_comment_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(max_length=100, verbose_name='评论目标'),
        ),
    ]
