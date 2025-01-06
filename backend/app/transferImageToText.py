import os
import pytesseract
import fitz  # PyMuPDF for PDF processing
from pathlib import Path

UPLOAD_FOLDER = "D:\\DaiHoc\\ForthYear\\chatbot\\backend\\app\\uploads"
DATA_FOLDER = "D:\\DaiHoc\\ForthYear\\chatbot\\backend\\app\\data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# Set Tesseract executable path (adjust to your system's path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf_with_images(upload_folder=UPLOAD_FOLDER, data_folder=DATA_FOLDER):
    # Ensure data folder exists
    os.makedirs(data_folder, exist_ok=True)

    for filename in os.listdir(upload_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(upload_folder, filename)
            text_output = ""

            # Process the PDF
            pdf_doc = fitz.open(pdf_path)
            for page_num, page in enumerate(pdf_doc):
                # Attempt to extract text directly
                text = page.get_text()
                if text.strip():
                    text_output += text
                else:
                    # If no text is found, perform OCR
                    pix = page.get_pixmap()
                    image_path = os.path.join(upload_folder, f"{Path(filename).stem}_page_{page_num}.png")
                    pix.save(image_path)
                    try:
                        ocr_text = pytesseract.image_to_string(image_path, lang="vie")  # Adjust the language as needed
                        text_output += ocr_text
                    except Exception as e:
                        print(f"Error during OCR on page {page_num}: {e}")
                    finally:
                        os.remove(image_path)  # Clean up temporary image file

            # Save extracted text to the data folder
            if text_output.strip():
                txt_filename = os.path.join(data_folder, f"{Path(filename).stem}.txt")
                with open(txt_filename, "w", encoding="utf-8") as txt_file:
                    txt_file.write(text_output)
                print(f"Extracted and saved text for {filename}")

if __name__ == "__main__":
    extract_text_from_pdf_with_images()
