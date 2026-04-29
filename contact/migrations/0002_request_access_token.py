import uuid
from django.db import migrations, models


def populate_tokens(apps, schema_editor):
    Request = apps.get_model('contact', 'Request')
    for req in Request.objects.all():
        req.access_token = uuid.uuid4()
        req.save(update_fields=['access_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        # Step 1: add nullable (no unique yet)
        migrations.AddField(
            model_name='request',
            name='access_token',
            field=models.UUIDField(null=True, blank=True),
        ),
        # Step 2: fill unique UUIDs for existing rows
        migrations.RunPython(populate_tokens, migrations.RunPython.noop),
        # Step 3: make it non-null and unique
        migrations.AlterField(
            model_name='request',
            name='access_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
