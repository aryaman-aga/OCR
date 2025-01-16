from PIL import Image
import pytesseract
import re
import cv2
import numpy as np
import os
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path

# Configure Tesseract path for Mac
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def convert_pdf_to_images(pdf_path):
    """Convert PDF to list of images."""
    try:
        return convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return []
def process_page(page, is_temp=False):
    """Process a single page/image with all checks."""
    if is_temp:
        temp_path = 'temp_page.png'
        page.save(temp_path)
        image_path = temp_path
    else:
        image_path = page
    
    results = {
        'text': pytesseract.image_to_string(page),
        'spacing_ok': True,
        'fonts_ok': True,
        'has_qr': False
    }
    
    # Run existing checks
    analyze_spacing(image_path)
    analyze_fonts(image_path)
    results['has_qr'] = check_qr_barcode(image_path)
    
    if is_temp:
        os.remove(temp_path)
    
    return results

def extract_text(file_path):
    """Extract text from image or PDF."""
    if file_path.lower().endswith('.pdf'):
        pages = convert_pdf_to_images(file_path)
        return '\n'.join(pytesseract.image_to_string(page) for page in pages)
    return pytesseract.image_to_string(Image.open(file_path))



def validate_aadhaar(text):
    """Validate Aadhaar number."""
    match = re.search(r"\b\d{4} \d{4} \d{4}\b", text)
    if not match:
        return None, "No valid Aadhaar pattern found"
    return match.group(), None

def validate_pan(text):
    """Validate PAN number."""
    match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b", text)
    if not match:
        return None, "No valid PAN pattern found"
    return match.group(), None

def analyze_spacing(image_path):
    """Analyze character spacing."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 10:
        print("Warning: Unusual character spacing detected")

def analyze_fonts(image_path):
    """Analyze font consistency."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    pixel_density = np.sum(binary == 255) / binary.size
    if pixel_density < 0.1 or pixel_density > 0.9:
        print("Warning: Unusual font characteristics detected")

def check_qr_barcode(image_path):
    """Check for QR codes or barcodes."""
    image = Image.open(image_path)
    decoded_objects = decode(image)
    return len(decoded_objects) > 0

def verify_document(file_path):
    """Verify if document is Aadhaar or PAN card."""
    if not os.path.exists(file_path):
        return "Error: File not found"

    print(f"Processing document: {file_path}")
    
    # Extract text and run validations
    text = extract_text(file_path)
    print("Extracted text:", text)
    
    if not text:
        return "Error: No text could be extracted"

    # Check for Aadhaar
    aadhaar_number, aadhaar_error = validate_aadhaar(text)
    if aadhaar_number:
        print(f"Valid Aadhaar Found: {aadhaar_number}")
        return "Aadhaar Verified"

    # Check for PAN
    pan_number, pan_error = validate_pan(text)
    if pan_number:
        print(f"Valid PAN Found: {pan_number}")
        return "PAN Verified"

    return f"Invalid Document:\nAadhaar Error: {aadhaar_error}\nPAN Error: {pan_error}"

    # Check for Aadhaar
    aadhaar_number, aadhaar_error = validate_aadhaar(text)
    if aadhaar_number:
        print(f"Valid Aadhaar Found: {aadhaar_number}")
        analyze_spacing(image_path)
        analyze_fonts(image_path)
        if check_qr_barcode(image_path):
            print("QR/Barcode found - additional verification passed")
        return "Aadhaar Verified"

    # Check for PAN
    pan_number, pan_error = validate_pan(text)
    if pan_number:
        print(f"Valid PAN Found: {pan_number}")
        analyze_spacing(image_path)
        analyze_fonts(image_path)
        return "PAN Verified"

    # If neither matched, return detailed error
    return f"Invalid Document:\nAadhaar Error: {aadhaar_error}\nPAN Error: {pan_error}"

# Example Usage
if __name__ == "__main__":
    file_path = "test/aadhaar_or_pan_card_image.jpg"  # Can be PDF or image
    result = verify_document(file_path)
    print("\nFinal Result:", result)