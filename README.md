# DocuFlex

**A fusion of "Document" and "Flexibility," emphasizing adaptability and versatile document processing.**

DocuFlex is a Django-based REST API designed to handle various operations on images and PDFs. With features like file uploads, metadata extraction, and file manipulation, DocuFlex simplifies document processing workflows.

---

## Features

- Upload and manage image and PDF files.
- Retrieve metadata for images and PDFs.
- Perform operations such as image rotation and PDF-to-image conversion.
- RESTful API with structured error handling and validation.
- Fully Dockerized for streamlined deployment and testing.

---

## API Endpoints

### File Management

- **`POST /api/upload/`**  
  Upload image and PDF files (in base64 format) to the server.

- **`GET /api/images/`**  
  Retrieve a list of all uploaded images.

- **`GET /api/pdfs/`**  
  Retrieve a list of all uploaded PDFs.

- **`GET /api/images/{id}/`**  
  Fetch details of a specific image, such as its file path, dimensions, and color channels.

- **`GET /api/pdfs/{id}/`**  
  Fetch details of a specific PDF, including its file path, number of pages, and page dimensions.

- **`DELETE /api/images/{id}/`**  
  Delete a specific image by its ID.

- **`DELETE /api/pdfs/{id}/`**  
  Delete a specific PDF by its ID.

### File Operations

- **`POST /api/rotate/`**  
  Rotate an image by a specified angle and return the rotated image.  
  **Request Body**: `{ "image_id": <id>, "angle": <degrees> }`

- **`POST /api/convert-pdf-to-image/`**  
  Convert a specific PDF into an image and return the result.  
  **Request Body**: `{ "pdf_id": <id> }`

---

## Documentation

### Postman Documentation

For detailed API requests and responses, visit the [Postman Documentation](https://documenter.getpostman.com/view/29804612/2sAYJ9Beh3).

### Live API Endpoints

The API is hosted on PythonAnywhere and can be accessed at:  
[DocuFlex API](https://docuflex.pythonanywhere.com/api/)

---
