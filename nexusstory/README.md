# NexusStory 👻
### A Django CYOA (Choose Your Own Adventure) Engine

A haunted mansion story built with pure Django — templates, models, views, sessions, forms, admin, and CSV export. Built for an FSD course demonstrating the full Django MVT pattern.

---

## Benchmark
This project is compared against [`dvndrsn/cyoa-story`](https://github.com/dvndrsn/cyoa-story), a Django + GraphQL + React CYOA app. NexusStory covers far more of Django's native features (templates, sessions, forms, admin) while keeping the same core concept.

---

## Features
- 🎮 Playable CYOA game with branching choices (14 scenes, multiple endings)
- 🗄️ Full DB-backed story graph (Scene → Choice → Scene)
- 👤 Session-based player progress tracking
- 🛠️ Customized Django Admin for story authoring
- 📋 ModelForm with custom validation (scene suggestion)
- 📊 Stats page
- 📁 CSV export of the full story map (Non-HTML content)
- 🗺️ Story Map using Generic ListView + DetailView

---

## Setup

```bash
# 1. Clone or unzip the project
cd nexusstory

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install Django
pip install django

# 4. Run migrations
python manage.py migrate

# 5. Load the story content
python manage.py loaddata adventure/fixtures/story.json

# 6. Create a superuser (for Admin access)
python manage.py createsuperuser

# 7. Run the dev server
python manage.py runserver
```

Then open: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin

---

## Project Structure

```
nexusstory/
├── manage.py
├── nexusstory/               # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── adventure/                # Main app
    ├── models.py             # Scene, Choice, PlayerSession
    ├── views.py              # All views (function + class-based)
    ├── urls.py               # URL routing
    ├── admin.py              # Customized admin
    ├── forms.py              # ModelForm with validation
    ├── fixtures/
    │   └── story.json        # Pre-built haunted mansion story
    ├── templates/adventure/
    │   ├── base.html         # Template inheritance base
    │   ├── home.html
    │   ├── scene.html        # Core gameplay
    │   ├── scene_list.html   # Generic ListView
    │   ├── scene_detail.html # Generic DetailView
    │   ├── suggest.html      # ModelForm page
    │   └── stats.html
    └── static/adventure/
        ├── css/style.css
        └── js/main.js
```

---

## Syllabus Coverage

| Topic | Where |
|---|---|
| MVC/MVT Pattern | Entire project structure |
| URL mapping / Loose coupling | `adventure/urls.py` included in `nexusstory/urls.py` |
| Views | `views.py` — function views + CBVs |
| Templates & Inheritance | `base.html` extended by all templates |
| Template tags & filters | `linebreaks`, `pluralize`, `date` filters in templates |
| Models & DB | `models.py` — Scene, Choice, PlayerSession |
| Data access (insert/update/delete/select) | `views.py` — PlayerSession CRUD |
| Admin Interface (customized) | `admin.py` — inline choices, list_editable, fieldsets |
| ModelForms & custom validation | `forms.py` + `suggest.html` |
| Generic Views | `SceneListView`, `SceneDetailView` in `views.py` |
| Non-HTML content (CSV) | `export_story_csv` view |
| Sessions | `get_player_session()` helper + `PlayerSession` model |
| URLConf includes | Root `urls.py` includes `adventure.urls` |
