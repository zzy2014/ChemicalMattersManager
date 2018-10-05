from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CCensoreStatesView, CCensorePatternsView, CFormStatesView
from .views import CAddMatterDetailsView

urlpatterns = [
    url(r'showOneTable/$', views.showOneTable, name='showOneTable'),
    url(r'showTwoTables/$', views.showTwoTables, name='showTwoTables'),
    url(r'censoreStates/$', CCensoreStatesView.as_view(), name='censoreStates'),
    url(r'censoreStates/(?P<intTypeId>[0-9]+)/?$', CCensoreStatesView.as_view(), name='deleteCensoreStates'),
    url(r'censorePatterns/$', CCensorePatternsView.as_view(), name='censorePatterns'),
    url(r'censorePatterns/(?P<intTypeId>[0-9]+)/?$', CCensorePatternsView.as_view(), name='deleteCensorePatterns'),
    url(r'formStates/$', CFormStatesView.as_view(), name='formStates'),
    url(r'formStates/(?P<intTypeId>[0-9]+)/?$', CFormStatesView.as_view(), name='deleteFormStates'),
    url(r'delTempMatterDetails/$', views.delTempMatterDetails, name='delTempMatterDetails'),
    url(r'addMatterDetails/$', CAddMatterDetailsView.as_view(), name='addMatterDetails'),
    url(r'addMatterDetails/(?P<intTypeId>[0-9]+)/?$', CAddMatterDetailsView.as_view(), name='deleteAddMatterDetails'),
    url(r'upLoadImportForm/$', views.upLoadImportForm, name='upLoadImportForm'),
]

