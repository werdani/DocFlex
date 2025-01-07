from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from api.models import UploadedPDF
from django.core.files.uploadedfile import SimpleUploadedFile

class TestPDFListView(TestCase):
    def setUp(self):
        # Initialize the APIClient and set the URL for the PDFListView
        self.client = APIClient()
        self.url = reverse('pdf-list')  

    def test_get_pdf_list(self):
        # Create a sample PDF to be returned by the PDFListView
        pdf = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        UploadedPDF.objects.create(file=pdf)
        
        # Send GET request to the PDF list endpoint
        response = self.client.get(self.url)

        # Assert that the status code is 200 (OK) when the PDF list is returned successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the uploaded PDF data
        self.assertGreater(len(response.data), 0)  # Ensure there is at least one PDF in the response
        self.assertIn("id", response.data[0])  # Ensure the 'id' field is present in the response data

    def test_no_pdfs(self):
        # Ensure the endpoint handles the case when no PDFs are uploaded
        response = self.client.get(self.url)

        # Assert that the status code is 200 (OK) when no PDFs are available
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data is an empty list
        self.assertEqual(response.data, [])
