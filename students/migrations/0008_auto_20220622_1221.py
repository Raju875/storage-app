# Generated by Django 2.2.28 on 2022-06-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20220622_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='height_feet',
            field=models.IntegerField(blank=True, default=0, verbose_name='Height Feet'),
        ),
        migrations.AlterField(
            model_name='album',
            name='height_inch',
            field=models.IntegerField(blank=True, default=0, verbose_name='Height Inch'),
        ),
    ]
