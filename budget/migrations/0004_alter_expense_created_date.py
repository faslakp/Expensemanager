# Generated by Django 5.1 on 2024-10-29 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_expense_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
