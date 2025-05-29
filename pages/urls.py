from django.urls import path
from .views import IndexView, AboutView

urlpatterns = [
    
    path('', IndexView.as_view(), name='pages-HomePage'),
    path('about/', AboutView.as_view(), name='pages-AboutPage'),
]
