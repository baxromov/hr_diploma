from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainTemplate.as_view(), name="backoffice-main"),
    path('xodimlar', views.StaffListTemplate.as_view(), name="staff"),
    path('xodimlar/create', views.StaffCreate.as_view(), name="staff_create"),
    path('xodimlar/<int:pk>', views.StaffUpdate.as_view(), name="staff-detail"),
    # path('xodimlar/update/<int:pk>', views.StaffUpdate.as_view(), name="staff-update"),
    path('table', views.TableTemplate.as_view(), name="table"),
    path('position/create', views.PositionCreateView.as_view(), name="position_create"),
    path('position', views.PositionListView.as_view(), name="position"),
    path('position/update/<int:pk>', views.PositionUpdateView.as_view(), name="position_update"),
    path('position/delete/<int:pk>', views.PositionDeleteView.as_view(), name="position_delete"),
    path('login', views.LoginPage.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('registration', views.Registration.as_view(), name="registration"),
]

# Department URL
urlpatterns += [
    path('department', views.DepartmentListView.as_view(), name='department'),
    path('department/create', views.DepartmentCreateView.as_view(), name='department_create'),
    path('department/update/<int:pk>', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('department/delete/<int:pk>', views.DepartmentDeleteView.as_view(), name='department_delete'),
]
