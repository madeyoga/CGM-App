# Generated by Django 3.1.4 on 2020-12-12 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='barang',
            name='harga_preview',
            field=models.CharField(default='Rp. <django.db.models.fields.BigIntegerField>', max_length=16),
        ),
    ]
