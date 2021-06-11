from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

router = routers.DefaultRouter()
router.register('flow', views.FlowModelViewSet)
router.register('staff', views.StaffModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('login', ObtainAuthToken.as_view()),
    path('logout', views.LogoutAPIView.as_view(), name='logout_api'),
    # path('staff', views.StaffRetrieveAPIView.as_view(), name='staff_api'),
    path('token/obtain', views.JWTTokenObtainView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
    path('token/refresh', views.JWTTokenRefreshView.as_view()),
]
