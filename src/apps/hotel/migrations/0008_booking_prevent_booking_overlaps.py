from django.contrib.postgres.operations import BtreeGistExtension
import django.contrib.postgres.constraints
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_booking_booking_index'),
    ]

    operations = [
        BtreeGistExtension(),
        migrations.AddConstraint(
            model_name='booking',
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(expressions=[('room', '='), (models.Func('start_date', 'end_date', function='daterange'), '&&')], name='prevent_booking_overlaps'),
        ),
    ]
