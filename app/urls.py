from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app.project_bot import BotAPIView

# bot url

urlpatterns = [
    path('bot/<str:tok>/', csrf_exempt(BotAPIView.as_view()))
]
