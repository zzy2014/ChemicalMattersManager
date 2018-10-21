from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CFinancesView

urlpatterns = [
    url(r'showOneTable/$', views.showOneTable, name='showOneTable'),
    url(r'showTwoTables/$', views.showTwoTables, name='showTwoTables'),
    url(r'finances/$', CFinancesView.as_view(), name='finances'),
    url(r'finances/(?P<intTypeId>[0-9]+)/?$', CFinancesView.as_view(), name='deleteFinances'),
]

