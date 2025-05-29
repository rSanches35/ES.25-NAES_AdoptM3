from django.urls import path

from .views import StateCreate, CityCreate, AddressCreate
from .views import StateUpdate, CityUpdate, AddressUpdate
from .views import StateDelete, CityDelete, AddressDelete
from .views import StateList, CityList, AddressList

urlpatterns = [
    
    path('create/state', StateCreate.as_view(), name='records-CreateState'),
    path('update/state/<int:pk>', StateUpdate.as_view(), name='records-UpdateState'),
    path('delete/state/<int:pk>', StateDelete.as_view(), name='records-DeleteState'),
    path('list/state', StateList.as_view(), name='records-ListState'),

    path('create/city', CityCreate.as_view(), name='records-CreateCity'),
    path('update/city/<int:pk>', CityUpdate.as_view(), name='records-UpdateCity'),
    path('delete/city/<int:pk>', CityDelete.as_view(), name='records-DeleteCity'),
    path('list/city', CityList.as_view(), name='records-ListCity'),

    path('create/address', AddressCreate.as_view(), name='records-CreateAddress'),
    path('update/address/<int:pk>', AddressUpdate.as_view(), name='records-UpdateAddress'),
    path('delete/address/<int:pk>', AddressDelete.as_view(), name='records-DeleteAddress'),
    path('list/address', AddressList.as_view(), name='records-ListAddress'),
]
