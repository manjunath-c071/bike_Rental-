# Auto-generated migration for schema adjustments

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='payment',
            new_name='payments_payment_created_idx',
            old_name='payments_pa_created_1a2b3c_idx',
        ),
        migrations.RenameIndex(
            model_name='payment',
            new_name='payments_payment_status_idx',
            old_name='payments_pa_status_4d5e6f_idx',
        ),
        migrations.RenameIndex(
            model_name='payment',
            new_name='payments_payment_user_idx',
            old_name='payments_pa_user_i_7a8b9c_idx',
        ),
    ]
