from django.db import models


class Scene(models.Model):
    """
    A single scene/page in the story.
    Each scene has text, an optional image, and can be a start or ending node.
    This is the core 'node' in our story graph.
    """
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="The narrative text shown to the player for this scene.")
    image_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional URL to an image representing this scene."
    )
    atmosphere = models.CharField(
        max_length=50,
        choices=[
            ('normal', 'Normal'),
            ('tense', 'Tense'),
            ('terrifying', 'Terrifying'),
            ('calm', 'Calm'),
            ('mysterious', 'Mysterious'),
        ],
        default='normal',
        help_text="Controls the visual mood/styling of the scene."
    )
    is_start = models.BooleanField(
        default=False,
        help_text="Mark exactly ONE scene as the starting point of the story."
    )
    is_ending = models.BooleanField(
        default=False,
        help_text="Ending scenes have no choices — the story concludes here."
    )
    ending_type = models.CharField(
        max_length=20,
        choices=[
            ('none', 'Not an ending'),
            ('good', 'Good Ending'),
            ('bad', 'Bad Ending'),
            ('neutral', 'Neutral Ending'),
        ],
        default='none',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        prefix = ""
        if self.is_start:
            prefix = "[START] "
        elif self.is_ending:
            prefix = f"[{self.ending_type.upper()} END] "
        return f"{prefix}{self.title}"

    class Meta:
        ordering = ['id']


class Choice(models.Model):
    """
    A directed edge from one Scene to another.
    Each choice belongs to a scene (the 'from' node) and points to a next_scene (the 'to' node).
    """
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name='choices',
        help_text="The scene this choice appears on."
    )
    text = models.CharField(
        max_length=300,
        help_text="The button label the player clicks (e.g. 'Go upstairs')."
    )
    next_scene = models.ForeignKey(
        Scene,
        on_delete=models.SET_NULL,
        null=True,
        related_name='incoming_choices',
        help_text="Where this choice leads."
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Controls the display order of choices on a scene."
    )

    def __str__(self):
        return f'"{self.text}" → {self.next_scene}'

    class Meta:
        ordering = ['order', 'id']


class PlayerSession(models.Model):
    """
    Tracks a single player's playthrough.
    Linked to Django's session framework so each browser tab has its own progress.
    Stores the full path taken as a record.
    """
    session_key = models.CharField(max_length=40, unique=True)
    current_scene = models.ForeignKey(
        Scene,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    scenes_visited = models.ManyToManyField(
        Scene,
        related_name='visited_by',
        blank=True,
        help_text="All scenes this player has visited during their playthrough."
    )
    started_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Session {self.session_key[:8]}... | Scene: {self.current_scene}"

    class Meta:
        verbose_name = "Player Session"
        verbose_name_plural = "Player Sessions"
