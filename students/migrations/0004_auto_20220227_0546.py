# Generated by Django 2.2.27 on 2022-02-27 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20220224_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportcard',
            name='grade',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Grade'),
        ),
        migrations.AlterField(
            model_name='specialservice',
            name='grade',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Grade'),
        ),
    ]
