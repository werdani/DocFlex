from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from api.models import UploadedImage

class TestRotateImageEndpoint(APITestCase):
    valid_payload = {
        'id': 1,  # Example image ID
        'angle': 90  # Example rotation angle
    }

    def setUp(self):
        # Create a valid image using PIL
        image = Image.new('RGB', (100, 100), color='red')  # Create a red image of size 100x100
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')  # Save the image into the BytesIO object
        image_file.seek(0)  # Go to the start of the BytesIO object
        
        # Create an image in the database
        self.image = UploadedImage.objects.create(id=1, file=SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg'))

    def test_rotate_image_success(self):
        url = reverse('rotate-image')
        response = self.client.post(url, self.valid_payload, format='json')

        print(response.data)  # Debugging response data to check any issues
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Image rotated successfully.')

    def test_rotate_image_invalid_angle(self):
        invalid_payload = {
            'id': 1,
            'angle': 'invalid_angle'  # Invalid angle value
        }
        url = reverse('rotate-image')
        response = self.client.post(url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Angle must be a valid integer.')

    def test_rotate_image_missing_parameters(self):
        incomplete_payload = {
            'id': 1  # Missing 'angle'
        }
        url = reverse('rotate-image')
        response = self.client.post(url, incomplete_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Angle must be a valid integer.')

    def test_rotate_image_not_found(self):
        invalid_payload = {
            'id': 9999,  # ID that doesn't exist
            'angle': 90
        }
        url = reverse('rotate-image')
        response = self.client.post(url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Image not found.")
