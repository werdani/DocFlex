from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PyPDF2 import PdfWriter
from io import BytesIO
from api.models import UploadedPDF

class TestPDFDetailView(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a sample PDF for testing
        pdf_buffer = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)  # Standard letter size
        writer.write(pdf_buffer)
        pdf_buffer.seek(0)

        pdf_file = SimpleUploadedFile("test.pdf", pdf_buffer.read(), content_type="application/pdf")
        self.uploaded_pdf = UploadedPDF.objects.create(file=pdf_file)

        # Set the URL for the PDF detail view, with the PDF's primary key (id)
        self.url = reverse('pdf-detail', kwargs={'pk': self.uploaded_pdf.pk})

    def test_retrieve_pdf_metadata(self):
        # Simulate a GET request to retrieve PDF metadata
        response = self.client.get(self.url)

        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that metadata is returned
        self.assertIn("number_of_pages", response.data)
        self.assertIn("page_width", response.data)
        self.assertIn("page_height", response.data)

    def test_retrieve_pdf_metadata_error(self):
        # Mock an invalid file path
        self.uploaded_pdf.file = None
        self.uploaded_pdf.save()

        response = self.client.get(self.url)

        # Check if the status code is 500 (Internal Server Error)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Assert that the error message is as expected
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Unable to read PDF metadata: The 'file' attribute has no file associated with it.")

    def test_pdf_not_found(self):
        # Send a GET request for a non-existing PDF ID
        url = reverse('pdf-detail', kwargs={'pk': 9999})  # Assuming this ID doesn't exist
        response = self.client.get(url)

        # Assert that the status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
