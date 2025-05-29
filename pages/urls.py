from django.urls import path
from .views import IndexView, AboutView

urlpatterns = [
    
    path('', IndexView.as_view(), name='Home Page'),
    path('about/', AboutView.as_view(), name='About Page'),
]
