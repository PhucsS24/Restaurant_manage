from django.urls import path
from . import views
# from .views import UserLoginAPIView
urlpatterns = [
    path('register/', views.register),
    path('login/', views.login, name='login')
    
]
