from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CMatterUnitsView, CMatterStatesView, CPurityLevelsView, CMatterTypesView
from .views import CStoreRoomsView

urlpatterns = [
    url(r'showRightPage/$', views.showRightPage, name='showRightPage'),
    url(r'matterUnits/$', CMatterUnitsView.as_view(), name='matterUnits'),
    url(r'matterUnits/(?P<intTypeId>[0-9]+)/?$', CMatterUnitsView.as_view(), name='deleteMatterUnits'),
    url(r'matterStates/$', CMatterStatesView.as_view(), name='matterStates'),
    url(r'matterStates/(?P<intTypeId>[0-9]+)/?$', CMatterStatesView.as_view(), name='deleteMatterStates'),
    url(r'purityLevels/$', CPurityLevelsView.as_view(), name='PurityLevels'),
    url(r'purityLevels/(?P<intTypeId>[0-9]+)/?$', CPurityLevelsView.as_view(), name='deletePurityLevels'),
    url(r'matterTypes/$', CMatterTypesView.as_view(), name='matterTypes'),
    url(r'matterTypes/(?P<intTypeId>[0-9]+)/?$', CMatterTypesView.as_view(), name='deleteMatterTypes'),
    url(r'storeRooms/$', CStoreRoomsView.as_view(), name='StoreRooms'),
    url(r'storeRooms/(?P<intTypeId>[0-9]+)/?$', CStoreRoomsView.as_view(), name='deleteStoreRooms'),
]

