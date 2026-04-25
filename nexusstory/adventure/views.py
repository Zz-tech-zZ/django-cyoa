import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib import messages

from .models import Scene, Choice, PlayerSession
from .forms import SceneSuggestForm


# ─────────────────────────────────────────
#  Helper: get or create the player's session record
# ─────────────────────────────────────────

def get_player_session(request):
    """
    Uses Django's session framework to find or create a PlayerSession
    tied to this browser. This covers the Sessions topic from Unit 4.
    """
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    player, created = PlayerSession.objects.get_or_create(session_key=session_key)
    return player


# ─────────────────────────────────────────
#  Home / Landing page
# ─────────────────────────────────────────

def home(request):
    """Simple landing page. Shows story title and a Start button."""
    player = get_player_session(request)
    context = {
        'player': player,
        'has_progress': player.current_scene is not None and not player.is_complete,
    }
    return render(request, 'adventure/home.html', context)


# ─────────────────────────────────────────
#  Start / Restart the game
# ─────────────────────────────────────────

def start_game(request):
    """
    Finds the scene marked is_start=True and drops the player there.
    Resets any existing progress for this session.
    """
    try:
        start_scene = Scene.objects.get(is_start=True)
    except Scene.DoesNotExist:
        messages.error(request, "The story has no starting scene yet. Ask an admin to set one!")
        return redirect('home')

    player = get_player_session(request)
    player.current_scene = start_scene
    player.is_complete = False
    player.scenes_visited.clear()
    player.scenes_visited.add(start_scene)
    player.save()

    return redirect('scene', scene_id=start_scene.id)


# ─────────────────────────────────────────
#  Core game view — display a scene
# ─────────────────────────────────────────

def scene_view(request, scene_id):
    """
    The main game loop. Renders the current scene with its choices.
    Also handles the POST when a player clicks a choice button.

    Demonstrates: URL mapping, views, template rendering, model queries.
    """
    scene = get_object_or_404(Scene, id=scene_id)
    player = get_player_session(request)

    # Sync the player's current position
    player.current_scene = scene
    if scene.is_ending:
        player.is_complete = True
    player.scenes_visited.add(scene)
    player.save()

    choices = scene.choices.select_related('next_scene').all()

    context = {
        'scene': scene,
        'choices': choices,
        'player': player,
        'visited_count': player.scenes_visited.count(),
    }
    return render(request, 'adventure/scene.html', context)


# ─────────────────────────────────────────
#  Handle choice selection (POST)
# ─────────────────────────────────────────

def make_choice(request, choice_id):
    """
    Processes the player's choice and redirects to the next scene.
    Using POST for choices (not GET) is the correct HTTP semantics
    since it's a state-changing action.
    """
    if request.method != 'POST':
        return redirect('home')

    choice = get_object_or_404(Choice, id=choice_id)

    if choice.next_scene:
        return redirect('scene', scene_id=choice.next_scene.id)
    else:
        messages.warning(request, "That path leads nowhere... yet.")
        return redirect('scene', scene_id=choice.scene.id)


# ─────────────────────────────────────────
#  Scene browser — Generic Class-Based View (ListView)
#  Covers: Generic Views topic from Unit 4
# ─────────────────────────────────────────

class SceneListView(ListView):
    """
    Lists all scenes in the story — useful as a 'story map' page.
    Uses Django's built-in generic ListView.
    """
    model = Scene
    template_name = 'adventure/scene_list.html'
    context_object_name = 'scenes'
    paginate_by = 10

    def get_queryset(self):
        return Scene.objects.prefetch_related('choices').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_scenes'] = Scene.objects.count()
        context['total_choices'] = Choice.objects.count()
        context['ending_count'] = Scene.objects.filter(is_ending=True).count()
        return context


# ─────────────────────────────────────────
#  Scene detail — Generic Class-Based View (DetailView)
# ─────────────────────────────────────────

class SceneDetailView(DetailView):
    """
    Read-only detail view of a scene (for the story map, not gameplay).
    """
    model = Scene
    template_name = 'adventure/scene_detail.html'
    context_object_name = 'scene'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.choices.select_related('next_scene').all()
        context['incoming'] = self.object.incoming_choices.select_related('scene').all()
        return context


# ─────────────────────────────────────────
#  Suggestion form — ModelForms topic from Unit 3
# ─────────────────────────────────────────

def suggest_scene(request):
    """
    Lets players submit scene/story suggestions.
    Demonstrates: Form processing, ModelForms, custom validation.
    """
    if request.method == 'POST':
        form = SceneSuggestForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            # Mark it as not a start/ending — it's a draft suggestion
            suggestion.is_start = False
            suggestion.is_ending = False
            suggestion.save()
            messages.success(request, "Your scene suggestion was submitted! The story master will review it.")
            return redirect('suggest_scene')
    else:
        form = SceneSuggestForm()

    return render(request, 'adventure/suggest.html', {'form': form})


# ─────────────────────────────────────────
#  CSV Export — Non-HTML content (Unit 4)
# ─────────────────────────────────────────

def export_story_csv(request):
    """
    Exports the full story graph as a CSV file.
    Covers the 'Generating Non-HTML content' topic (Chapter 9).
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nexusstory_map.csv"'

    writer = csv.writer(response)
    writer.writerow(['Scene ID', 'Scene Title', 'Is Start', 'Is Ending', 'Ending Type', 'Choice Text', 'Leads To Scene ID', 'Leads To Scene Title'])

    scenes = Scene.objects.prefetch_related('choices__next_scene').all()
    for scene in scenes:
        choices = scene.choices.all()
        if choices:
            for choice in choices:
                writer.writerow([
                    scene.id,
                    scene.title,
                    scene.is_start,
                    scene.is_ending,
                    scene.ending_type,
                    choice.text,
                    choice.next_scene.id if choice.next_scene else '',
                    choice.next_scene.title if choice.next_scene else 'DEAD END',
                ])
        else:
            writer.writerow([
                scene.id,
                scene.title,
                scene.is_start,
                scene.is_ending,
                scene.ending_type,
                '(no choices)',
                '',
                '',
            ])

    return response


# ─────────────────────────────────────────
#  Stats page
# ─────────────────────────────────────────

def stats_view(request):
    """Shows live stats about player sessions and story coverage."""
    player = get_player_session(request)
    total_scenes = Scene.objects.count()
    visited = player.scenes_visited.count()
    percent = round((visited / total_scenes * 100), 1) if total_scenes > 0 else 0

    context = {
        'player': player,
        'total_scenes': total_scenes,
        'visited': visited,
        'percent': percent,
        'total_players': PlayerSession.objects.count(),
        'completed_players': PlayerSession.objects.filter(is_complete=True).count(),
    }
    return render(request, 'adventure/stats.html', context)
