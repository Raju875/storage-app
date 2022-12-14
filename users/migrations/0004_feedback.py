# Generated by Django 2.2.28 on 2022-07-14 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_verificationcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.CharField(choices=[('0', 'inactive'), ('1', 'active')], default='1', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
                'ordering': ['-id'],
            },
        ),
    ]
