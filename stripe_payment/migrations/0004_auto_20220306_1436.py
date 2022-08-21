# Generated by Django 2.2.26 on 2022-03-06 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stripe_payment', '0003_auto_20220305_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_id', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Token ID')),
                ('payment_method_id', models.CharField(blank=True, max_length=120, null=True, verbose_name='Payment method id')),
                ('fingerprint', models.CharField(blank=True, max_length=120, null=True, verbose_name='Fingerprint')),
                ('is_default', models.CharField(choices=[('0', 'no'), ('1', 'yes')], default=0, max_length=2)),
                ('status', models.CharField(choices=[('0', 'inactive'), ('1', 'active')], default=1, max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payment Method',
                'verbose_name_plural': 'Payment Methods',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='StripePayment',
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_payment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Stripe Payment',
                'verbose_name_plural': 'Stripe Payments',
                'ordering': ['-id'],
            },
        ),
        migrations.RemoveField(
            model_name='stripecustomerpayment',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomerPaymentMethod',
        ),
        migrations.DeleteModel(
            name='StripeCustomerPayment',
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_method', to='stripe_payment.StripePayment'),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_method', to=settings.AUTH_USER_MODEL),
        ),
    ]
