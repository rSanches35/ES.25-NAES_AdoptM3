from django.urls import path

from .views import StateCreate, CityCreate
from .views import StateUpdate

urlpatterns = [
    
    path('create/state', StateCreate.as_view(), name='records-CreateState'),
    path('update/state/<int:pk>', StateUpdate.as_view(), name='records-UpdateState'),

    path('create/city', CityCreate.as_view(), name='records-CreateCity'),
]
