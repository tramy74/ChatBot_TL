# backend/app/utils/image_processing.py
import os
import cv2
from paddleocr import PaddleOCR
from PIL import Image

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def segment_and_extract_text_from_image(image_path):
    """
    Segment the image to find text areas, extract text from those areas, 
    and return as a single combined text.
    
    :param image_path: Path to the image file
    :return: Extracted text as a string
    """
    # Load the image
    image = cv2.imread(image_path)

    # Segment the image and extract text
    # For example, you might be using contours, thresholding, etc., to find text areas
    text_segments = []
    
    # Example placeholder segmentation code (replace with actual segmentation logic)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        segmented_image = image[y:y+h, x:x+w]
        
        # Convert segment to PIL Image for OCR
        pil_image = Image.fromarray(segmented_image)
        result = ocr.ocr(pil_image, cls=True)
        
        # Extract text from OCR results
        for line in result[0]:
            for word_info in line:
                text_segments.append(word_info[1][0])  # word_info[1][0] contains detected text

    # Combine all text segments into a single string
    extracted_text = " ".join(text_segments)
    return extracted_text
