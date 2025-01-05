# Imports standard libraries
##..
# Imports core Django libraries
from django.db import models

# Imports third-party libraries
from PIL import Image
from PyPDF2 import PdfReader
# Imports from your apps
##..

class UploadedImage(models.Model):
    file = models.ImageField(upload_to='uploads/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}.image'
    
    def get_metadata(self):
        with Image.open(self.file.path) as img:
            return {
                "location": self.file.path,
                "width": img.width,
                "height": img.height,
                "channels": len(img.getbands())
            }

class UploadedPDF(models.Model):
    file = models.FileField(upload_to='uploads/pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}.PDF'

    def get_metadata(self):
        try:
            reader = PdfReader(self.file.path)
            return {
                "location": self.file.path,
                "number_of_pages": len(reader.pages),
                "page_width": reader.pages[0].mediabox.width,
                "page_height": reader.pages[0].mediabox.height
            }
        except Exception as e:
            raise ValueError(f"Unable to read PDF metadata: {e}")