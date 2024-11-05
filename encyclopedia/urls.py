from django.urls import path

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.create_page, name="create"),
    path("<str:title>", views.get_page, name="page"),
]