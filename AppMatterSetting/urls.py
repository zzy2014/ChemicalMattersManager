from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CMatterUnitsView, CMatterStatesView, CPurityLevelsView, CMatterTypesView
from .views import CStoreRoomsView, CMattersView, CMatterAlertsView, CMatterMinRemainsView
from .views import CMatterAccessBlocksView

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
    url(r'matters/$', CMattersView.as_view(), name='matters'),
    url(r'matters/(?P<intTypeId>[0-9]+)/?$', CMattersView.as_view(), name='deleteMatters'),
    url(r'matterAlerts/$', CMatterAlertsView.as_view(), name='matterAlerts'),
    url(r'matterAlerts/(?P<intTypeId>[0-9]+)/?$', CMatterAlertsView.as_view(), name='deleteMatterAlerts'),
    url(r'matterMinRemains/$', CMatterMinRemainsView.as_view(), name='matterMinRemains'),
    url(r'matterMinRemains/(?P<intTypeId>[0-9]+)/?$', CMatterMinRemainsView.as_view(), name='deleteMatterMinRemains'),
    url(r'matterAccessBlocks/$', CMatterAccessBlocksView.as_view(), name='matterAccessBlocks'),
    url(r'matterAccessBlocks/(?P<intTypeId>[0-9]+)/?$', CMatterAccessBlocksView.as_view(), name='deleteMatterAccessBlocks'),

]

