# Generated manually on 2025-09-04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_adoption_created_by_adoptionrelic_created_by'),
    ]

    operations = [
        # Alterar o campo register_date do Client para auto_now_add
        migrations.AlterField(
            model_name='client',
            name='register_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        # Alterar o campo last_activity do Client para auto_now
        migrations.AlterField(
            model_name='client',
            name='last_activity',
            field=models.DateTimeField(auto_now=True),
        ),
        # Tornar o campo address do Client opcional
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.PROTECT, to='records.address'),
        ),
        # Alterar o campo adoption_date do Adoption para auto_now_add
        migrations.AlterField(
            model_name='adoption',
            name='adoption_date',
            field=models.DateField(auto_now_add=True),
        ),
        # Alterar o campo payment_status do Adoption para BooleanField
        migrations.AlterField(
            model_name='adoption',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
