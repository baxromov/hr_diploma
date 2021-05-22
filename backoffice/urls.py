from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainTemplate.as_view(), name="backoffice-main"),
    path('table', views.TableTemplate.as_view(), name="table"),
    path('login', views.LoginPage.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('registration', views.Registration.as_view(), name="registration"),
]

# Staff
urlpatterns += [
    path('xodimlar', views.StaffListTemplate.as_view(), name="staff"),
    path('xodimlar/create', views.StaffCreate.as_view(), name="staff_create"),
    path('xodimlar/<int:pk>', views.StaffUpdate.as_view(), name="staff-detail"),
]

# Position
urlpatterns += [
    path('position/create', views.PositionCreateView.as_view(), name="position_create"),
    path('position', views.PositionListView.as_view(), name="position"),
    path('position/update/<int:pk>', views.PositionUpdateView.as_view(), name="position_update"),
    path('position/delete/<int:pk>', views.PositionDeleteView.as_view(), name="position_delete"),
]

# Department URL
urlpatterns += [
    path('department', views.DepartmentListView.as_view(), name='department'),
    path('department/create', views.DepartmentCreateView.as_view(), name='department_create'),
    path('department/update/<int:pk>', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('department/delete/<int:pk>', views.DepartmentDeleteView.as_view(), name='department_delete'),
]

# Salary
urlpatterns += [
    path('salary/<int:pk>', views.SalaryListView.as_view(), name='salary'),
    path('salary/create', views.SalaryCreateView.as_view(), name='salary_create'),
    path('salary/update/<int:pk>', views.SalaryUpdateView.as_view(), name='salary_update'),
    path('salary/delete/<int:pk>', views.SalaryDeleteView.as_view(), name='salary_delete'),
]
