from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from api.models import UploadedImage
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
import tempfile

class TestImageDetailView(TestCase):
    def setUp(self):
        # Initialize the APIClient
        self.client = APIClient()

        # Create a temporary file to simulate a real image upload
        temp_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        image = PILImage.new("RGB", (100, 100))  # Create a dummy image
        image.save(temp_image, format="JPEG")
        temp_image.seek(0)  # Rewind the file pointer

        # Use the temporary file for the UploadedImage instance
        with open(temp_image.name, "rb") as img_file:
            self.uploaded_image = UploadedImage.objects.create(
                file=SimpleUploadedFile(temp_image.name, img_file.read(), content_type="image/jpeg")
            )

        # Set the URL for the image detail view
        self.url = reverse('image-detail', kwargs={'pk': self.uploaded_image.pk})

    def test_retrieve_image_metadata(self):
        # Simulate a GET request to retrieve image metadata
        response = self.client.get(self.url)

        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that metadata is returned
        self.assertIn("location", response.data)
        self.assertIn("width", response.data)
        self.assertIn("height", response.data)
        self.assertIn("channels", response.data)

    def test_retrieve_image_metadata_error(self):
        # Mock an invalid file path
        self.uploaded_image.file = None
        self.uploaded_image.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Image file is missing or inaccessible")

    def test_image_not_found(self):
        # Send a GET request for a non-existing image ID
        url = reverse('image-detail', kwargs={'pk': 9999})  # Assuming this ID doesn't exist
        response = self.client.get(url)

        # Assert that the status code is 404 (Not Found) when the image does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
