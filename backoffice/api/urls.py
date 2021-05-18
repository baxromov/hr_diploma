from django.urls import path, include
from rest_framework import routers

from . import views
from .views import CustomObtainAuthToken

router = routers.DefaultRouter()
router.register('flow', views.FlowModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', CustomObtainAuthToken.as_view()),
    # path('login123', include('rest_framework.urls')),
]
