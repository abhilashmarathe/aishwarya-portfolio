from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Category
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower


@login_required
def dashboard(request):
    total_projects = Project.objects.count()
    total_categories = Category.objects.count()
    featured_count = Project.objects.filter(featured=True).count()
    published_count = Project.objects.filter(is_published=True).count()
    projects = Project.objects.all()

    return render(request, "dashboard.html", {
        "total_projects": total_projects,
        "total_categories": total_categories,
        "featured_count": featured_count,
        "published_count": published_count,
        "projects": projects,
    })


from django.http import JsonResponse

def home(request):
    category_id = request.GET.get("category")

    # Only categories that have at least one published project
    categories = Category.objects.filter(
        project__is_published=True
    ).distinct().order_by(Lower("name"))

    projects = Project.objects.filter(is_published=True)

    if category_id:
        projects = projects.filter(category__id=category_id)

    # AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = []
        for project in projects:
            data.append({
                "id": project.id,
                "title": project.title,
                "image": project.cover_image.url,
            })
        return JsonResponse({"projects": data})

    return render(request, "index.html", {
        "projects": projects,
        "categories": categories
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, is_published=True)

    return render(request, "project_detail.html", {
        "project": project
    })


@login_required
def upload_project(request):
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        new_category_name = request.POST.get("new_category")
        cover_image = request.FILES.get("cover_image")
        featured = request.POST.get("featured") == "on"

        # ---- Category Logic ----
        if new_category_name:
            category, created = Category.objects.get_or_create(
                name=new_category_name.strip()
            )
        elif category_id:
            category = get_object_or_404(Category, id=category_id)
        else:
            return render(request, "upload.html", {
                "categories": categories,
                "error": "Please select or create a category."
            })

        # ---- Create Project ----
        Project.objects.create(
            title=title,
            description=description,
            category=category,
            cover_image=cover_image,
            featured=featured
        )

        return redirect("dashboard")

    return render(request, "upload.html", {
        "categories": categories
    })

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    categories = Category.objects.all()

    if request.method == "POST":
        project.title = request.POST.get("title")
        project.description = request.POST.get("description")
        project.category_id = request.POST.get("category")
        project.featured = True if request.POST.get("featured") else False
        project.is_published = True if request.POST.get("is_published") else False

        if request.FILES.get("cover_image"):
            project.cover_image = request.FILES.get("cover_image")

        project.save()
        return redirect("dashboard")

    return render(request, "edit_project.html", {
        "project": project,
        "categories": categories
    })

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect("dashboard")


