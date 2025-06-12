from django import forms
from .models import Blog, Feature, TechStack, Learning
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control select2-multiple",
            }
        ),
        required=False,
    )

    tech_stack = forms.ModelMultipleChoiceField(
        queryset=TechStack.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control select2-multiple",
            }
        ),
        required=False,
    )

    learnings = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 6,
                "style": "min-height: 150px;",
                "placeholder": "Enter what you learned (one point per line)",
            }
        ),
        required=True,
    )

    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "image",
            "features",
            "tech_stack",
            "project_url",
            "github_url",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Basic field configurations
        self.fields["title"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter project title",
            }
        )

        self.fields["content"].widget = CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"}, config_name="default"
        )

        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )

        self.fields["project_url"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "https://your-project-url.com",
            }
        )

        self.fields["github_url"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "https://github.com/username/repository",
            }
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

            # Handle learnings - split by newlines and create Learning objects
            learning_points = [
                point.strip()
                for point in self.cleaned_data["learnings"].split("\n")
                if point.strip()
            ]
            instance.learnings.clear()
            for point in learning_points:
                learning = Learning.objects.create(description=point)
                instance.learnings.add(learning)

        return instance
