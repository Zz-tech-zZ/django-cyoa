from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField(help_text='The narrative text shown to the player for this scene.')),
                ('image_url', models.URLField(blank=True, help_text='Optional URL to an image representing this scene.', null=True)),
                ('atmosphere', models.CharField(
                    choices=[('normal', 'Normal'), ('tense', 'Tense'), ('terrifying', 'Terrifying'), ('calm', 'Calm'), ('mysterious', 'Mysterious')],
                    default='normal', max_length=50,
                    help_text='Controls the visual mood/styling of the scene.'
                )),
                ('is_start', models.BooleanField(default=False, help_text='Mark exactly ONE scene as the starting point of the story.')),
                ('is_ending', models.BooleanField(default=False, help_text='Ending scenes have no choices — the story concludes here.')),
                ('ending_type', models.CharField(
                    blank=True, default='none', max_length=20,
                    choices=[('none', 'Not an ending'), ('good', 'Good Ending'), ('bad', 'Bad Ending'), ('neutral', 'Neutral Ending')]
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['id']},
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300, help_text="The button label the player clicks (e.g. 'Go upstairs').")),
                ('order', models.PositiveIntegerField(default=0, help_text='Controls the display order of choices on a scene.')),
                ('scene', models.ForeignKey(
                    help_text='The scene this choice appears on.',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='choices', to='adventure.scene'
                )),
                ('next_scene', models.ForeignKey(
                    help_text='Where this choice leads.',
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name='incoming_choices', to='adventure.scene'
                )),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='PlayerSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40, unique=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('current_scene', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='adventure.scene'
                )),
                ('scenes_visited', models.ManyToManyField(
                    blank=True,
                    help_text='All scenes this player has visited during their playthrough.',
                    related_name='visited_by', to='adventure.scene'
                )),
            ],
            options={'verbose_name': 'Player Session', 'verbose_name_plural': 'Player Sessions'},
        ),
    ]
