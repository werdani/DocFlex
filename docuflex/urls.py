# Imports standard libraries
##..
# Imports core Django libraries
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path

# Imports third-party libraries
##..

# Imports from your apps
##..

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
