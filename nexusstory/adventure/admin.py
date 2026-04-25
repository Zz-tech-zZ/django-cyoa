from django.contrib import admin
from .models import Scene, Choice, PlayerSession


class ChoiceInline(admin.TabularInline):
    """
    Inline editor for Choices within the Scene admin.
    This lets you add/edit all choices for a scene on the same page.
    Demonstrates: Customizing Admin Interfaces (Chapter 6).
    """
    model = Choice
    extra = 3  # Show 3 empty rows to fill in by default
    fields = ['text', 'next_scene', 'order']
    autocomplete_fields = []
    fk_name = 'scene'


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    """
    Custom admin for Scene model.
    Story authors use this to build the entire game without touching code.
    """
    list_display = ['id', 'title', 'atmosphere', 'is_start', 'is_ending', 'ending_type', 'choice_count', 'created_at']
    list_filter = ['is_start', 'is_ending', 'atmosphere', 'ending_type']
    search_fields = ['title', 'body']
    list_editable = ['atmosphere', 'is_start', 'is_ending']
    readonly_fields = ['created_at']
    inlines = [ChoiceInline]

    fieldsets = (
        ('Scene Content', {
            'fields': ('title', 'body', 'image_url', 'atmosphere')
        }),
        ('Story Graph Settings', {
            'fields': ('is_start', 'is_ending', 'ending_type'),
            'description': 'Control where this scene sits in the story flow.'
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def choice_count(self, obj):
        return obj.choices.count()
    choice_count.short_description = '# Choices'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Standalone admin for Choices — useful for bulk management."""
    list_display = ['id', 'scene', 'text', 'next_scene', 'order']
    list_filter = ['scene']
    search_fields = ['text', 'scene__title', 'next_scene__title']
    list_editable = ['order']


@admin.register(PlayerSession)
class PlayerSessionAdmin(admin.ModelAdmin):
    """
    Read-only view of player sessions for monitoring playthroughs.
    """
    list_display = ['session_key_short', 'current_scene', 'is_complete', 'scenes_visited_count', 'started_at', 'last_active']
    list_filter = ['is_complete']
    readonly_fields = ['session_key', 'current_scene', 'scenes_visited', 'started_at', 'last_active']

    def session_key_short(self, obj):
        return obj.session_key[:12] + '...'
    session_key_short.short_description = 'Session Key'

    def scenes_visited_count(self, obj):
        return obj.scenes_visited.count()
    scenes_visited_count.short_description = 'Scenes Visited'


# Customize the admin site header
admin.site.site_header = "NexusStory Admin"
admin.site.site_title = "NexusStory"
admin.site.index_title = "Story Management"
