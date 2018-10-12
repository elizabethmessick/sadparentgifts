from django.urls import path
from . import views

urlpatterns = [
    path('', views.discover_gifts, name='discover_gifts'),
    path('about/', views.about, name='about'),
    path('gifts/<int:gift_id>', views.gifts_detail, name='gifts_detail'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('gifts/create/', views.GiftCreate.as_view(), name='gifts_create'),
    path('gifts/<int:pk>/update/', views.GiftUpdate.as_view(), name='gifts_update'),
    path('gifts/<int:pk>/delete/', views.GiftDelete.as_view(), name='gifts_delete'),
]
