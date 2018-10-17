from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CCensoreStatesView, CCensorePatternsView, CFormStatesView
from .views import CAddMatterDetailsView, CImportFormsView

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
    url(r'calculateCensorePattern/$', views.calculateCensorePattern, name='calculateCensorePattern'),
    url(r'importForms/$', CImportFormsView.as_view(), name='importForms'),
    url(r'importForms/(?P<intTypeId>[0-9]+)/?$', CImportFormsView.as_view(), name='deleteImportForms'),
    url(r'createNewImportForm/$', views.createNewImportForm, name='createNewImportForm'),
    url(r'showCensoreDialog/$', views.showCensoreDialog, name='showCensoreDialog'),
    url(r'censoreImportForm/$', views.censoreImportForm, name='censoreImportForm'),
]

