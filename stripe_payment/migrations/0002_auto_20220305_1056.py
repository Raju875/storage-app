# Generated by Django 2.2.26 on 2022-03-05 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpaymentmethod',
            name='fingerprint',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Fingerprint'),
        ),
        migrations.AlterField(
            model_name='customerpaymentmethod',
            name='payment_method',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Payment method'),
        ),
    ]
