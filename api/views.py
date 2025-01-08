# Imports standard libraries
from PIL import Image
from pdf2image import convert_from_path
import os
from django.conf import settings

# Imports core Django libraries
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Imports third-party libraries
##..

# Imports from your apps
from .models import UploadedImage, UploadedPDF
from .serializers import UploadedImageSerializer, UploadedPDFSerializer


@api_view(['POST'])
def upload_file(request):
    # Check if a file was uploaded
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        if file.content_type.startswith('image'):
            instance = UploadedImage.objects.create(file=file)
            return Response(UploadedImageSerializer(instance).data, status=status.HTTP_201_CREATED)
        elif file.content_type == 'application/pdf':
            instance = UploadedPDF.objects.create(file=file)
            return Response(UploadedPDFSerializer(instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
    except AttributeError:
        return Response({"error": "Invalid file format."}, status=status.HTTP_400_BAD_REQUEST)
    
class ImageListView(generics.ListAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

class PDFListView(generics.ListAPIView):
    queryset = UploadedPDF.objects.all()
    serializer_class = UploadedPDFSerializer

class ImageDetailView(generics.RetrieveDestroyAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            metadata = instance.get_metadata()
            return Response(metadata, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PDFDetailView(generics.RetrieveDestroyAPIView):
    queryset = UploadedPDF.objects.all()
    serializer_class = UploadedPDFSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            metadata = instance.get_metadata()
            return Response(metadata, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def rotate_image(request):
    image_id = request.data.get('id')
    angle = request.data.get('angle')

    # Validate that 'id' is provided
    if not image_id:
        return Response({"error": "Image ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the angle is a valid integer
    try:
        angle = int(angle)
    except (ValueError, TypeError):
        return Response({"error": "Angle must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

    # Try to get the image from the database
    try:
        image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

    # Try to open the image and rotate it
    try:
        img = Image.open(image.file.path)
        img = img.rotate(angle)
        img.save(image.file.path)  # You can save it to a different location or handle it differently if needed
        return Response({"message": "Image rotated successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def convert_pdf_to_image(request):
    pdf_id = request.data.get('id')
    try:
        pdf = UploadedPDF.objects.get(id=pdf_id)
        images = convert_from_path(pdf.file.path)
        output_paths = []

        # Define the output directory inside the MEDIA folder
        output_dir = os.path.join(settings.MEDIA_ROOT, 'converted_pdf')
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

        for i, img in enumerate(images):
            output_path = os.path.join(output_dir, f"{pdf_id}_page_{i+1}.jpg")
            img.save(output_path, 'JPEG')
            # Convert to relative URL for client usage
            relative_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
            output_paths.append(os.path.join(settings.MEDIA_URL, relative_path))

        return Response({"images": output_paths}, status=status.HTTP_200_OK)
    except UploadedPDF.DoesNotExist:
        return Response({"error": "PDF not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

