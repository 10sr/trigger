from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = "trigger"
urlpatterns = [
    path("", views.index, name="index"),
    path("note/", RedirectView.as_view(url="from/web"), name="note"),
    path("note/from/web", views.note_from_web, name="note_from_web"),
    path("note/from/web/post", views.note_from_web_post, name="note_from_web_post"),
]
