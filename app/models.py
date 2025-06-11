from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TechStack(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Learning(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class Blog(models.Model):

    image = models.ImageField(upload_to="media/", blank=True, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    features = models.ManyToManyField(Feature)
    tech_stack = models.ManyToManyField(TechStack)
    learnings = models.ManyToManyField(Learning)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    github_url = models.URLField(blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]  # Order by creation date, newest first
