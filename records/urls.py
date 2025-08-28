from django.urls import path

from .views import StateCreate, CityCreate, AddressCreate, ClientCreate, RelicCreate, AdoptionCreate, AdoptionRelicCreate
from .views import StateUpdate, CityUpdate, AddressUpdate, ClientUpdate, RelicUpdate, AdoptionUpdate, AdoptionRelicUpdate
from .views import StateDelete, CityDelete, AddressDelete, ClientDelete, RelicDelete, AdoptionDelete, AdoptionRelicDelete
from .views import StateList, CityList, AddressList, ClientList, RelicList, AdoptionList, AdoptionRelicList

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

    path('create/client', ClientCreate.as_view(), name='records-CreateClient'),
    path('update/client/<int:pk>', ClientUpdate.as_view(), name='records-UpdateClient'),
    path('delete/client/<int:pk>', ClientDelete.as_view(), name='records-DeleteClient'),
    path('list/client', ClientList.as_view(), name='records-ListClient'),

    path('create/relic', RelicCreate.as_view(), name='records-CreateRelic'),
    path('update/relic/<int:pk>', RelicUpdate.as_view(), name='records-UpdateRelic'),
    path('delete/relic/<int:pk>', RelicDelete.as_view(), name='records-DeleteRelic'),
    path('list/relic', RelicList.as_view(), name='records-ListRelic'),

    path('create/adoption', AdoptionCreate.as_view(), name='records-CreateAdoption'),
    path('update/adoption/<int:pk>', AdoptionUpdate.as_view(), name='records-UpdateAdoption'),
    path('delete/adoption/<int:pk>', AdoptionDelete.as_view(), name='records-DeleteAdoption'),
    path('list/adoption', AdoptionList.as_view(), name='records-ListAdoption'),

    path('create/adoptionrelic', AdoptionRelicCreate.as_view(), name='records-CreateAdoptionRelic'),
    path('update/adoptionrelic/<int:pk>', AdoptionRelicUpdate.as_view(), name='records-UpdateAdoptionRelic'),
    path('delete/adoptionrelic/<int:pk>', AdoptionRelicDelete.as_view(), name='records-DeleteAdoptionRelic'),
    path('list/adoptionrelic', AdoptionRelicList.as_view(), name='records-ListAdoptionRelic'),
]
