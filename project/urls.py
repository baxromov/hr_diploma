from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('app.urls')),
    path('api/v1/', include('backoffice.api.urls')),
    path('backoffice/', include('backoffice.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_title = "HR"
admin.site.site_header = "Algorithm-Getaway HR"
admin.site.index_title = "Algorithm-Getaway HRga hush kelibsiz"
