from django.urls import path
from . import views

urlpatterns = [
    path('', views.discover_gifts, name='discover_gifts'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:id>/', views.profile, name='profile'),


]
