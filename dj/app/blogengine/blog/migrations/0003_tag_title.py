# Generated by Django 2.0.7 on 2021-05-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210527_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='title',
            field=models.CharField(default='dg', max_length=50),
            preserve_default=False,
        ),
    ]
