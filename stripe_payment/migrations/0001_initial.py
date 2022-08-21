# Generated by Django 2.2.26 on 2022-03-05 03:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeCustomerPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=200, verbose_name='Customer id')),
                ('payment_method_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Payment Method id')),
                ('subscription_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Subscription id')),
                ('paid_until', models.CharField(blank=True, max_length=200, null=True, verbose_name='Paid until')),
                ('no_of_subscriptions', models.IntegerField(default=0, verbose_name='No of subscription')),
                ('status', models.CharField(choices=[('0', 'inactive'), ('1', 'active')], default=1, max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Stripe Customer Payment',
                'verbose_name_plural': 'Stripe Customer Payments',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CustomerPaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=120, verbose_name='Payment method')),
                ('fingerprint', models.CharField(max_length=120, verbose_name='Fingerprint')),
                ('is_default', models.CharField(choices=[('0', 'no'), ('1', 'yes')], default=0, max_length=2)),
                ('status', models.CharField(choices=[('0', 'inactive'), ('1', 'active')], default=1, max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_payment_method', to='stripe_payment.StripeCustomerPayment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_payment_method', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Payment Method',
                'verbose_name_plural': 'Customer Payment Methods',
                'ordering': ['-id'],
            },
        ),
    ]
