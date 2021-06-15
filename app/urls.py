from django.urls import path
from app import views


# StaffLoginTemplateView
urlpatterns = [
    path('staff-login', views.StaffLoginTemplateView.as_view(), name="staff_login"),
    path('staff-training', views.StaffPageTemplateView.as_view(), name="staff_training"),
]
