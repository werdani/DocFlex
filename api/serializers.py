# Imports standard libraries
##..
# Imports core Django libraries
from rest_framework import serializers

# Imports third-party libraries
##..
# Imports from your apps
from .models import UploadedImage, UploadedPDF



class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'

class UploadedPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPDF
        fields = '__all__'