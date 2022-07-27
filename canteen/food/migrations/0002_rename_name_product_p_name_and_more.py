# Generated by Django 4.0.6 on 2022-07-27 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='p_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='home_delivery',
        ),
        migrations.AddField(
            model_name='order',
            name='take_away',
            field=models.CharField(choices=[('yes', 'yes')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Todayspl', 'Todays special')], max_length=200, null=True),
        ),
    ]