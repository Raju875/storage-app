# Generated by Django 2.2.27 on 2022-02-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20220224_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='Weight'),
        ),
    ]
