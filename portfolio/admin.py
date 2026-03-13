from django.contrib import admin
from .models import Category, Project, ProjectImage, Catalogue, Profile

class CatalogueInline(admin.TabularInline):
    model = Catalogue
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [CatalogueInline]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(Catalogue)
admin.site.register(Profile)
