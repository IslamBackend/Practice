from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.registration_view),
    path('login/', views.login_view),
    path('profile/', views.profile_view),
    path('logout/', views.logout_view),

]
