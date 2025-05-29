from django.urls import path

from .views import StateCreate, CityCreate
from .views import StateUpdate
from .views import StateDelete
from .views import StateList

urlpatterns = [
    
    path('create/state', StateCreate.as_view(), name='records-CreateState'),
    path('update/state/<int:pk>', StateUpdate.as_view(), name='records-UpdateState'),
    path('delete/state/<int:pk>', StateDelete.as_view(), name='records-DeleteState'),
    path('list/state', StateList.as_view(), name='records-ListState'),

    path('create/city', CityCreate.as_view(), name='records-CreateCity'),
]
