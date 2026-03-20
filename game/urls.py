from django.urls import path
from . import views


app_name = "game"
urlpatterns = [
    path("", views.start, name="start"),
    path("/prologue", views.prologue, name="prologue"),
    path("/stage1", views.stage1, name="stage1"),
    path("/stage2", views.stage2, name="stage2"),
    path("/stage3", views.stage3, name="stage3"),
    path("/epilogue", views.epilogue, name="epilogue"),
]