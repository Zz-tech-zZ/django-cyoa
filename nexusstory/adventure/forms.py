from django import forms
from .models import Scene


class SceneSuggestForm(forms.ModelForm):
    """
    A ModelForm that lets players suggest new scenes for the story.
    Demonstrates: ModelForms, custom validation (Unit 3).
    """

    class Meta:
        model = Scene
        fields = ['title', 'body', 'atmosphere', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Give your scene a title...',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 6,
                'placeholder': 'Describe what happens in this scene...',
            }),
            'atmosphere': forms.Select(attrs={
                'class': 'form-select',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com/image.jpg (optional)',
            }),
        }
        labels = {
            'body': 'Scene Description',
            'image_url': 'Image URL (optional)',
        }
        help_texts = {
            'atmosphere': 'This controls the mood/colour theme of the scene.',
            'body': 'Be descriptive — the player will read this when they arrive at your scene.',
        }

    def clean_title(self):
        """Custom validation: title must be at least 5 characters."""
        title = self.cleaned_data.get('title', '')
        if len(title) < 5:
            raise forms.ValidationError("Scene title must be at least 5 characters long.")
        return title

    def clean_body(self):
        """Custom validation: scene body must be at least 50 characters."""
        body = self.cleaned_data.get('body', '')
        if len(body) < 50:
            raise forms.ValidationError("Scene description must be at least 50 characters. Give us some atmosphere!")
        return body
