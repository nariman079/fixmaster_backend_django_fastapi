# Generated by Django 4.2.6 on 2024-05-16 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(editable=False, max_length=30, verbose_name='ID Телеграм')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона')),
                ('username', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя пользователя')),
                ('addidional_info', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительная информация')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(default='web_user', editable=False, max_length=30, verbose_name='ID Телеграм')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
                ('surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('image', models.ImageField(upload_to='master', verbose_name='Изображние')),
                ('gender', models.CharField(blank=True, choices=[('MEN', 'Мужчина'), ('WOMEN', 'Женщина')], default='MEN', max_length=30, null=True, verbose_name='Пол')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастера',
            },
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Типы оргинизаций')),
            ],
            options={
                'verbose_name': 'Тип организации',
                'verbose_name_plural': 'Типы организаций',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True, verbose_name='Название')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость')),
                ('min_time', models.IntegerField(blank=True, null=True, verbose_name='Минимальная длительность процедуры')),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.master')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(editable=False, max_length=30, verbose_name='ID Телеграм')),
                ('title', models.CharField(max_length=30, verbose_name='Название')),
                ('main_image', models.ImageField(upload_to='business', verbose_name='Заглавное изображение')),
                ('address', models.CharField(max_length=30, verbose_name='Адрес')),
                ('contact_phone', models.CharField(max_length=30, verbose_name='Номер телефона')),
                ('time_begin', models.TimeField(verbose_name='Начало рабочего дня')),
                ('time_end', models.TimeField(verbose_name='Конец рабочего дня')),
                ('work_schedule', models.CharField(max_length=30, verbose_name='График работы')),
                ('organization_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='src.organizationtype')),
            ],
            options={
                'verbose_name': 'Салон',
                'verbose_name_plural': 'Салоны',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(blank=True, null=True, verbose_name='Дата начала')),
                ('begin_time', models.TimeField(blank=True, null=True, verbose_name='Время начала')),
                ('status', models.CharField(blank=True, choices=[('New', 'Новый'), ('InProgress', 'В прогрессе'), ('Done', 'Закончено')], max_length=20, null=True, verbose_name='Статус')),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('payment_link', models.CharField(blank=True, max_length=500, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.customer', verbose_name='Клиент')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.master', verbose_name='Мастер')),
                ('services', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='src.service')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.AddField(
            model_name='master',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.organization', verbose_name='Организация'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Изображение')),
                ('priority', models.IntegerField(default=0, verbose_name='Приоритет')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.organization')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField(blank=True, null=True, verbose_name='Дата бронирования')),
                ('booking_time', models.TimeField(blank=True, null=True, verbose_name='Время бронирования')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.master')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирование',
            },
        ),
    ]
