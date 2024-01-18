from django.urls import path
from anime import views

urlpatterns = [
    path('', views.main_view),
    path('anime/', views.anime_list_view),
    path('anime/create/', views.anime_create_view),
    path('anime/<int:anime_id>/', views.anime_detail_view),
    path('anime/<int:anime_id>/update/', views.anime_update_view),
    path('anime/<int:anime_id>/delete/', views.anime_delete_view),
]
