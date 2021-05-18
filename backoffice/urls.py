from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainTemplate.as_view(), name="backoffice-main"),
    path('xodimlar', views.StaffListTemplate.as_view(), name="staff"),
    path('xodimlar/baxromov-shahzodbek', views.StaffDetailTemplate.as_view(), name="staff-detail"),
    path('table', views.TableTemplate.as_view(), name="table"),
    path('login', views.Login.as_view(), name="login"),
    path('registration', views.Registration.as_view(), name="registration"),

]
