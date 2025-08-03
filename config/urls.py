from django.contrib import admin
from django.urls import path, include, re_path
from django.http import  HttpResponse
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

def favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    path('', include('apps.frontend.urls')),
    re_path(r'^favicon.ico$', favicon), 
    path('admin/', admin.site.urls),  
    path('api/v1/', include([
        path('schema-viewer/', include('schema_viewer.urls')),
        path('auths/', include('apps.auths.urls')),
        path('subscription/', include('apps.subscription.urls')),
        path('exchange/', include('apps.exchange.urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
