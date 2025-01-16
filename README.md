# OCR-Based Aadhaar and PAN Card Validator

This project implements Optical Character Recognition (OCR) to extract and validate Aadhaar and PAN card information from images or PDF files. It uses the Tesseract OCR engine and additional libraries for text extraction, character spacing analysis, font consistency checks, and QR/barcode detection.

---

## **Features**
- Converts PDF documents to images for OCR processing.
- Extracts text from images or PDFs using Tesseract.
- Validates Aadhaar and PAN card formats using regular expressions.
- Analyzes character spacing and font consistency.
- Detects and verifies QR codes or barcodes.
- Configured for Mac systems but can be modified for other platforms.

---

## **Libraries Used**
The following Python libraries are used in this project:

1. **[Pillow (PIL)]**
   - Used for image handling and preprocessing.

2. **[pytesseract]**
   - Python wrapper for the Tesseract OCR engine to extract text from images.

3. **[re]**
   - For regular expression-based Aadhaar and PAN validation.

4. **[cv2 (OpenCV)]**
   - Used for character spacing and font consistency analysis.

5. **[numpy]**
   - For efficient image and pixel-level processing.

6. **[os]**
   - To handle file paths and manage temporary files.

7. **[pyzbar]**
   - For QR code and barcode detection.

8. **[pdf2image]**
   - Converts PDF files into images for OCR processing.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.7 or above.
- Tesseract installed on your system.
  - **For Mac Users:** Install Tesseract using Homebrew:
    ```bash
    brew install tesseract
    ```

### **2. Clone the Repository**
   ```bash
   git clone https://github.com/username/ocr-validator.git
   cd ocr-validator
