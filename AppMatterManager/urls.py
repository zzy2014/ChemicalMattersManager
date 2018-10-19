from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CCensoreStatesView, CCensorePatternsView, CFormStatesView
from .views import CImportMatterDetailsView, CImportFormsView, CExportMatterDetailsView, CExportFormsView
from .views import CPerchaseMatterDetailsView, CPerchaseFormsView, CReserveMatterDetailsView, CReserveFormsView

urlpatterns = [
    url(r'showOneTable/$', views.showOneTable, name='showOneTable'),
    url(r'showTwoTables/$', views.showTwoTables, name='showTwoTables'),
    url(r'censoreStates/$', CCensoreStatesView.as_view(), name='censoreStates'),
    url(r'censoreStates/(?P<intTypeId>[0-9]+)/?$', CCensoreStatesView.as_view(), name='deleteCensoreStates'),
    url(r'censorePatterns/$', CCensorePatternsView.as_view(), name='censorePatterns'),
    url(r'censorePatterns/(?P<intTypeId>[0-9]+)/?$', CCensorePatternsView.as_view(), name='deleteCensorePatterns'),
    url(r'formStates/$', CFormStatesView.as_view(), name='formStates'),
    url(r'formStates/(?P<intTypeId>[0-9]+)/?$', CFormStatesView.as_view(), name='deleteFormStates'),

    url(r'deleteFromOneTable/$', views.deleteFromOneTable, name='deleteFromOneTable'),
    url(r'calculateCensorePattern/$', views.calculateCensorePattern, name='calculateCensorePattern'),
    url(r'createNewForm/$', views.createNewForm, name='createNewForm'),
    url(r'showCensoreDialog/$', views.showCensoreDialog, name='showCensoreDialog'),
    url(r'censoreForm/$', views.censoreForm, name='censoreForm'),

    url(r'genPerchaseMatterDetails/$', views.genPerchaseMatterDetails, name='genPerchaseMatterDetails'),
    url(r'perchaseMatterDetails/$', CPerchaseMatterDetailsView.as_view(), name='perchaseMatterDetails'),
    url(r'perchaseMatterDetails/(?P<intTypeId>[0-9]+)/?$', CPerchaseMatterDetailsView.as_view(), name='deletePerchaseMatterDetails'),
    url(r'perchaseForms/$', CPerchaseFormsView.as_view(), name='perchaseForms'),
    url(r'perchaseForms/(?P<intTypeId>[0-9]+)/?$', CPerchaseFormsView.as_view(), name='deletePerchaseForms'),

    url(r'importMatterDetails/$', CImportMatterDetailsView.as_view(), name='importMatterDetails'),
    url(r'importMatterDetails/(?P<intTypeId>[0-9]+)/?$', CImportMatterDetailsView.as_view(), name='deleteImportMatterDetails'),
    url(r'importForms/$', CImportFormsView.as_view(), name='importForms'),
    url(r'importForms/(?P<intTypeId>[0-9]+)/?$', CImportFormsView.as_view(), name='deleteImportForms'),

    url(r'reserveMatterDetails/$', CReserveMatterDetailsView.as_view(), name='reserveMatterDetails'),
    url(r'reserveMatterDetails/(?P<intTypeId>[0-9]+)/?$', CReserveMatterDetailsView.as_view(), name='deleteReserveMatterDetails'),
    url(r'reserveForms/$', CReserveFormsView.as_view(), name='reserveForms'),
    url(r'reserveForms/(?P<intTypeId>[0-9]+)/?$', CReserveFormsView.as_view(), name='deleteReserveForms'),

    url(r'exportMatterDetails/$', CExportMatterDetailsView.as_view(), name='exportMatterDetails'),
    url(r'exportMatterDetails/(?P<intTypeId>[0-9]+)/?$', CExportMatterDetailsView.as_view(), name='deleteExportMatterDetails'),
    url(r'exportForms/$', CExportFormsView.as_view(), name='exportForms'),
    url(r'exportForms/(?P<intTypeId>[0-9]+)/?$', CExportFormsView.as_view(), name='deleteExportForms'),
]

