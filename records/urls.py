from django.urls import path

from .views import StateCreate, CityCreate, AddressCreate, ClientCreate, RelicCreate, AdoptionCreate, AdoptionRelicCreate
from .views import StateUpdate, CityUpdate, AddressUpdate, ClientUpdate, RelicUpdate, AdoptionUpdate, AdoptionRelicUpdate
from .views import StateDelete, CityDelete, AddressDelete, ClientDelete, RelicDelete, AdoptionDelete, AdoptionRelicDelete
from .views import StateList, CityList, AddressList, ClientList, RelicList, AdoptionList, AdoptionRelicList

app_name = 'records'

urlpatterns = [
    
    path('create/state', StateCreate.as_view(), name='StateCreate'),
    path('update/state/<int:pk>', StateUpdate.as_view(), name='StateUpdate'),
    path('delete/state/<int:pk>', StateDelete.as_view(), name='StateDelete'),
    path('list/state', StateList.as_view(), name='StateList'),

    path('create/city', CityCreate.as_view(), name='CityCreate'),
    path('update/city/<int:pk>', CityUpdate.as_view(), name='CityUpdate'),
    path('delete/city/<int:pk>', CityDelete.as_view(), name='CityDelete'),
    path('list/city', CityList.as_view(), name='CityList'),

    path('create/address', AddressCreate.as_view(), name='AddressCreate'),
    path('update/address/<int:pk>', AddressUpdate.as_view(), name='AddressUpdate'),
    path('delete/address/<int:pk>', AddressDelete.as_view(), name='AddressDelete'),
    path('list/address', AddressList.as_view(), name='AddressList'),

    path('create/client', ClientCreate.as_view(), name='ClientCreate'),
    path('update/client/<int:pk>', ClientUpdate.as_view(), name='ClientUpdate'),
    path('delete/client/<int:pk>', ClientDelete.as_view(), name='ClientDelete'),
    path('list/client', ClientList.as_view(), name='ClientList'),

    path('create/relic', RelicCreate.as_view(), name='RelicCreate'),
    path('update/relic/<int:pk>', RelicUpdate.as_view(), name='RelicUpdate'),
    path('delete/relic/<int:pk>', RelicDelete.as_view(), name='RelicDelete'),
    path('list/relic', RelicList.as_view(), name='RelicList'),

    path('create/adoption', AdoptionCreate.as_view(), name='AdoptionCreate'),
    path('update/adoption/<int:pk>', AdoptionUpdate.as_view(), name='AdoptionUpdate'),
    path('delete/adoption/<int:pk>', AdoptionDelete.as_view(), name='AdoptionDelete'),
    path('list/adoption', AdoptionList.as_view(), name='AdoptionList'),

    path('create/adoptionrelic', AdoptionRelicCreate.as_view(), name='AdoptionRelicCreate'),
    path('update/adoptionrelic/<int:pk>', AdoptionRelicUpdate.as_view(), name='AdoptionRelicUpdate'),
    path('delete/adoptionrelic/<int:pk>', AdoptionRelicDelete.as_view(), name='AdoptionRelicDelete'),
    path('list/adoptionrelic', AdoptionRelicList.as_view(), name='AdoptionRelicList'),
]
