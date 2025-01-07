from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from api.models import UploadedImage
from django.core.files.uploadedfile import SimpleUploadedFile

class TestImageListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('image-list') 

    def test_get_image_list(self):
        # Create a sample image to be returned by the ImageListView
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        UploadedImage.objects.create(file=image)
        
        # Send GET request to the image list endpoint
        response = self.client.get(self.url)

        # Assert that the status code is 200 (OK) when the image list is returned successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the uploaded image data
        self.assertGreater(len(response.data), 0)  # Ensure there is at least one image in the response
        self.assertIn("id", response.data[0])  # Ensure the 'id' field is present in the response data

    def test_no_images(self):
        # Ensure the endpoint handles the case when no images are uploaded
        response = self.client.get(self.url)

        # Assert that the status code is 200 (OK) when no images are available
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data is an empty list
        self.assertEqual(response.data, [])