from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from ChemicalMattersManager.settings import MEDIA_ROOT
from . import views
from .views import CMatterUnitsView

urlpatterns = [
    url(r'showRightPage/$', views.showRightPage, name='showRightPage'),
    url(r'matterUnits/$', CMatterUnitsView.as_view(), name='matterUnits'),
    url(r'matterUnits/(?P<intTypeId>[0-9]+)/?$', CMatterUnitsView.as_view(), name='deleteMatterUnits'),
]

