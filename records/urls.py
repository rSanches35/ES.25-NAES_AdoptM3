from django.urls import path

from .views import StateCreate, CityCreate
from .views import StateUpdate, CityUpdate
from .views import StateDelete, CityDelete
from .views import StateList, CityList

urlpatterns = [
    
    path('create/state', StateCreate.as_view(), name='records-CreateState'),
    path('update/state/<int:pk>', StateUpdate.as_view(), name='records-UpdateState'),
    path('delete/state/<int:pk>', StateDelete.as_view(), name='records-DeleteState'),
    path('list/state', StateList.as_view(), name='records-ListState'),

    path('create/city', CityCreate.as_view(), name='records-CreateCity'),
    path('update/city/<int:pk>', CityUpdate.as_view(), name='records-UpdateCity'),
    path('delete/city/<int:pk>', CityDelete.as_view(), name='records-DeleteCity'),
    path('list/city', CityList.as_view(), name='records-ListCity'),
]
