from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, default="Portfolio Owner")
    def __str__(self):
        return self.name
        
class Profile(models.Model):
    name = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)

class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="projects/")
    created_at = models.DateTimeField(auto_now_add=True)

    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")


class Catalogue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='catalogue_images')
    image = models.ImageField(upload_to='catalogue/')

    def __str__(self):
        return self.project.title
