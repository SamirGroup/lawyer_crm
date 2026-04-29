from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_case_notes_meeting'),
        ('contact', '0002_request_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreCaseMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='chat_files/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pre_messages', to='contact.request')),
            ],
            options={'ordering': ['timestamp']},
        ),
    ]
