from django.urls import path
from app import views

urlpatterns = [
    path('staff-login', views.StaffLoginTemplateView.as_view(), name="staff_login"),
    path('staff-login', views.StaffLoginTemplateView.as_view(), name="staff_login"),
    path('staff-training/<uuid:staff_uuid>/', views.StaffFormView.as_view(), name="staff_training"),
]
