from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registrations/', views.registrations_views, name='registrations'),
    path("logout", views.logout_view, name= "logout"),
]
