from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

class TestUploadFile(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('upload-file')

    def test_upload_image(self):
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(self.url, {'file': image})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)

    def test_upload_pdf(self):
        pdf = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        response = self.client.post(self.url, {'file': pdf})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)

    def test_upload_unsupported_file(self):
        txt = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        response = self.client.post(self.url, {'file': txt})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_upload_no_file(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "No file uploaded")  
