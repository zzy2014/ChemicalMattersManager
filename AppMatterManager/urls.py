from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CCensoreStatesView, CCensorePatternsView

urlpatterns = [
    url(r'showOneTable/$', views.showOneTable, name='showOneTable'),
    url(r'showTwoTables/$', views.showTwoTables, name='showTwoTables'),
    url(r'censoreStates/$', CCensoreStatesView.as_view(), name='censoreStates'),
    url(r'censoreStates/(?P<intTypeId>[0-9]+)/?$', CCensoreStatesView.as_view(), name='deleteCensoreStates'),
    url(r'censorePatterns/$', CCensorePatternsView.as_view(), name='censorePatterns'),
    url(r'censorePatterns/(?P<intTypeId>[0-9]+)/?$', CCensorePatternsView.as_view(), name='deleteCensorePatterns'),
]

