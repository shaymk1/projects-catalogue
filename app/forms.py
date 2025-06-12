from django import forms
from .models import Blog, Feature, TechStack, Learning
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogForm(forms.ModelForm):
    # Dynamically added fields for many-to-many relationships
    features = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter features (comma-separated)",
            }
        ),
        required=False,
        help_text="Enter features separated by commas",
    )
    tech_stack = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter technologies (comma-separated)",
            }
        ),
        required=False,
        help_text="Enter technologies separated by commas",
    )
    learnings = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter learnings (comma-separated)",
            }
        ),
        required=False,
        help_text="Enter learnings separated by commas",
    )

    class Meta:
        model = Blog
        fields = ["image", "title", "content", "project_url", "github_url"]
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter project name"}
            ),
            "project_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://your-project-url.com",
                }
            ),
            "github_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/username/repository",
                }
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

            # Handle many-to-many relationships
            # Features
            feature_names = [
                name.strip()
                for name in self.cleaned_data["features"].split(",")
                if name.strip()
            ]
            for name in feature_names:
                feature, _ = Feature.objects.get_or_create(name=name)
                instance.features.add(feature)

            # Tech Stack
            tech_names = [
                name.strip()
                for name in self.cleaned_data["tech_stack"].split(",")
                if name.strip()
            ]
            for name in tech_names:
                tech, _ = TechStack.objects.get_or_create(name=name)
                instance.tech_stack.add(tech)

            # Learnings
            learning_texts = [
                text.strip()
                for text in self.cleaned_data["learnings"].split(",")
                if text.strip()
            ]
            for text in learning_texts:
                learning, _ = Learning.objects.get_or_create(description=text)
                instance.learnings.add(learning)

        return instance
