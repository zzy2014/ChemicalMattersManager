from django.conf.urls import url
from . import views
from .views import CUserTypesView, CUserStatesView, CStudentTypesView
from .views import CAdministratorsView, CChiefCollegeLeadersView

urlpatterns = [
    url(r'loginVerify/$', views.loginVerify, name='loginVerify'),
    url(r'userHome/$', views.userHome, name='userHome'),
    url(r'userTypes/$', CUserTypesView.as_view(), name='userTypes'),
    url(r'userTypes/(?P<intTypeId>[0-9]+)/?$', CUserTypesView.as_view(), name='deleteUserType'),
    url(r'userStates/$', CUserStatesView.as_view(), name='userStates'),
    url(r'userStates/(?P<intTypeId>[0-9]+)/?$', CUserStatesView.as_view(), name='deleteUserState'),
    url(r'studentTypes/$', CStudentTypesView.as_view(), name='studentTypes'),
    url(r'studentTypes/(?P<intTypeId>[0-9]+)/?$', CStudentTypesView.as_view(), name='deleteStudentType'),
    url(r'administrators/$', CAdministratorsView.as_view(), name='administrators'),
    url(r'administrators/(?P<intTypeId>[0-9]+)/?$', CAdministratorsView.as_view(), name='administrators'),
    url(r'chiefCollegeLeaders/$', CChiefCollegeLeadersView.as_view(), name='chiefCollegeLeaders'),
    url(r'chiefCollegeLeaders/(?P<intTypeId>[0-9]+)/?$', CChiefCollegeLeadersView.as_view(), name='chiefCollegeLeaders'),
]

