from django.contrib import admin

# Register your models here.
from .models import UploadedPDF, UploadedImage

admin.site.register(UploadedPDF)
admin.site.register(UploadedImage)