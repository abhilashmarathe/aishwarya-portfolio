from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("upload/", views.upload_project, name="upload_project"),
    path("project/<int:pk>/", views.project_detail, name="project_detail"),
    path("edit/<int:pk>/", views.edit_project, name="edit_project"),
    path("delete/<int:pk>/", views.delete_project, name="delete_project"),

]