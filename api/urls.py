# Imports standard libraries
##..
# Imports core Django libraries
from django.urls import path

# Imports third-party libraries
##..

# Imports from your apps
from .views import (
    upload_file, ImageListView, PDFListView,
)

urlpatterns = [
    path('upload/', upload_file, name='upload-file'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('pdfs/', PDFListView.as_view(), name='pdf-list'),

]
