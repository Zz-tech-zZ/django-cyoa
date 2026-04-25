from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Game flow
    path('start/', views.start_game, name='start_game'),
    path('scene/<int:scene_id>/', views.scene_view, name='scene'),
    path('choose/<int:choice_id>/', views.make_choice, name='make_choice'),

    # Story map (Generic Views)
    path('map/', views.SceneListView.as_view(), name='scene_list'),
    path('map/<int:pk>/', views.SceneDetailView.as_view(), name='scene_detail'),

    # Community suggestion form
    path('suggest/', views.suggest_scene, name='suggest_scene'),

    # Non-HTML export
    path('export/csv/', views.export_story_csv, name='export_csv'),

    # Stats
    path('stats/', views.stats_view, name='stats'),
]
