# Generated by Django 3.1.6 on 2021-04-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0002_history_input_manufacturer_personal_product_product_output'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=20)),
                ('qty', models.IntegerField()),
                ('employee', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=20)),
                ('shelf_id', models.TextField(blank=True, max_length=50)),
                ('qty', models.IntegerField()),
                ('employee', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Group_analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(default='', max_length=20)),
                ('group', models.CharField(default='A', max_length=1)),
                ('profit', models.IntegerField(default=0)),
                ('month_qty', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='lost_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=20)),
                ('shelf_id', models.TextField(blank=True, max_length=50)),
                ('qty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50)),
                ('shop_name', models.CharField(max_length=50)),
                ('employee', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('date_sended', models.DateField(blank=True, default=None)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='preorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=20)),
                ('balance', models.IntegerField()),
                ('employee', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='product_shelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=20)),
                ('shelf_id', models.TextField(blank=True, max_length=50)),
                ('qty', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='saled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=20)),
                ('shop_name', models.CharField(max_length=50)),
                ('employee', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('qty', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code1_4', models.CharField(max_length=4)),
                ('code5_6', models.CharField(max_length=2)),
                ('code7_9', models.CharField(max_length=3)),
                ('code', models.TextField(blank=True, max_length=50)),
                ('value', models.IntegerField()),
                ('valueremain', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=50)),
                ('store_id', models.CharField(max_length=20)),
                ('store_t', models.TextField()),
                ('store_a', models.TextField()),
                ('store_city', models.TextField()),
                ('store_post', models.CharField(max_length=20)),
                ('store_email', models.EmailField(max_length=254)),
                ('store_phone', models.CharField(max_length=20)),
                ('store_desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='store_stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(max_length=20)),
                ('product_code', models.CharField(max_length=20)),
                ('qty', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='product_balance',
            field=models.IntegerField(default=0),
        ),
    ]
