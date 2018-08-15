from django.conf.urls import url
from . import views
from .views import CUserTypesView, CUserStatesView, CStudentTypesView
from .views import CAdministratorsView, CChiefCollegeLeadersView, CCollegeLeadersView
from .views import CTeachersView, CStudentsView, CFinancesView

urlpatterns = [
    url(r'register/$', views.register, name='register'),
    url(r'loginVerify/$', views.loginVerify, name='loginVerify'),
    url(r'userHome/$', views.userHome, name='userHome'),
    url(r'userTypes/$', CUserTypesView.as_view(), name='userTypes'),
    url(r'userTypes/(?P<intTypeId>[0-9]+)/?$', CUserTypesView.as_view(), name='deleteUserType'),
    url(r'userStates/$', CUserStatesView.as_view(), name='userStates'),
    url(r'userStates/(?P<intTypeId>[0-9]+)/?$', CUserStatesView.as_view(), name='deleteUserState'),
    url(r'studentTypes/$', CStudentTypesView.as_view(), name='studentTypes'),
    url(r'studentTypes/(?P<intTypeId>[0-9]+)/?$', CStudentTypesView.as_view(), name='deleteStudentType'),
    url(r'administrators/$', CAdministratorsView.as_view(), name='administrators'),
    url(r'administrators/(?P<intTypeId>[0-9]+)/?$', CAdministratorsView.as_view(), name='deleteAdministrators'),
    url(r'chiefCollegeLeaders/$', CChiefCollegeLeadersView.as_view(), name='chiefCollegeLeaders'),
    url(r'chiefCollegeLeaders/(?P<intTypeId>[0-9]+)/?$', CChiefCollegeLeadersView.as_view(), name='deleteChiefCollegeLeaders'),
    url(r'collegeLeaders/$', CCollegeLeadersView.as_view(), name='collegeLeaders'),
    url(r'collegeLeaders/(?P<intTypeId>[0-9]+)/?$', CCollegeLeadersView.as_view(), name='deleteCollegeLeaders'),
    url(r'teachers/$', CTeachersView.as_view(), name='teachers'),
    url(r'teachers/(?P<intTypeId>[0-9]+)/?$', CTeachersView.as_view(), name='deleteTeachers'),
    url(r'students/$', CStudentsView.as_view(), name='students'),
    url(r'students/(?P<intTypeId>[0-9]+)/?$', CStudentsView.as_view(), name='deleteStudents'),
    url(r'finances/$', CFinancesView.as_view(), name='finances'),
    url(r'finances/(?P<intTypeId>[0-9]+)/?$', CFinancesView.as_view(), name='deleteFinances'),
]

