from django.urls import path
from .views import IndexView, AboutView, SignUpView

urlpatterns = [
    
    path('', IndexView.as_view(), name='pages-HomePage'),
    path('about/', AboutView.as_view(), name='pages-AboutPage'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
