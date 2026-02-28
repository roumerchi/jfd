from django.contrib import admin
from django.urls import path, include
from supra import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('contacts.urls', 'contacts'), namespace='contacts')),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
    urlpatterns = [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema')),
    ] + urlpatterns
