# Generated by Django 5.2.1 on 2025-06-23 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0005_document_plain_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='session_id',
            field=models.CharField(blank=True, default=models.AutoField(primary_key=True, serialize=False), max_length=255),
        ),
    ]
