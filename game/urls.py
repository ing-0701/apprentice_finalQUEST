
from django.urls import path
from . import views


app_name = "game"
urlpatterns = [
    path("", views.start, name="start"),
    path("prologue/", views.prologue, name="prologue"),
    path("stage1/", views.stage1, name="stage1"),
    path("stage2/", views.stage2, name="stage2"),
    path("stage3/", views.stage3, name="stage3"),
    path("epilogue/", views.epilogue, name="epilogue"),
    path('api/dialogue/<str:stage_tag>/', views.DialogueView.as_view(), name='dialogue_api'),
    path('api/gatekeeper_reset/', views.GatekeeperResetView.as_view(), name='gatekeeper_reset_api'),
    path('api/gatekeeper_ask/<str:ask>/', views.GatekeeperView.as_view(), name='gatekeeper_api'),
    path('api/minister_reset/', views.MinisterResetView.as_view(), name='minister_reset_api'),
    path('api/minister_ask/<str:ask>/', views.MinisterView.as_view(), name='minister_api'),
    path('api/king_reset/', views.KingResetView.as_view(), name='king_reset_api'),
    path('api/king_ask/<str:ask>/', views.KingView.as_view(), name='king_api'),
]