from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('service_type', models.CharField(choices=[('classic', 'Оздоровительный'), ('relax', 'Релакс '), ('home', 'Выезд на дом')], max_length=20)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('duration', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
    ]
