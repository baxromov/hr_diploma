from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app.project_bot import BotAPIView
from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('departmets/', views.departments, name='departmets'),
#     path('question/<int:pk>', views.question, name='question'),
#     path('ajax_departmets/', views.ajax_dep, name='ajax_department'),
# ]

# bot url

urlpatterns = [
    path('bot/<str:token>/', csrf_exempt(BotAPIView.as_view()))
]
