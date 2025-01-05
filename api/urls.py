# Imports standard libraries
##..
# Imports core Django libraries
from django.urls import path

# Imports third-party libraries
##..

# Imports from your apps
from .views import (
    upload_file,
)

urlpatterns = [
    path('upload/', upload_file, name='upload-file'),

]
