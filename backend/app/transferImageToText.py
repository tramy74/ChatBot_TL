import os
import psycopg2
import openai
import pytesseract
import cv2
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

# Connect to PostgreSQL
def connect_to_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# Extract text from images in folders using OCR
def extract_text_from_images(main_folder='SachVan11'):
    hinh_folder = os.path.join(main_folder, 'Hinh')
    all_text = {}

    for image_folder in os.listdir(hinh_folder):
        folder_path = os.path.join(hinh_folder, image_folder)
        if os.path.isdir(folder_path):
            text_output = []
            print(f"Processing folder: {folder_path}")

            # Process each image file
            for paragraph_image_file in sorted(os.listdir(folder_path)):
                if paragraph_image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(folder_path, paragraph_image_file)
                    paragraph_image = cv2.imread(image_path)

                    if paragraph_image is not None:
                        # Extract text using pytesseract
                        paragraph_text = pytesseract.image_to_string(paragraph_image)
                        text_output.append(paragraph_text)

            # Join all extracted text from folder
            all_text[image_folder] = "\n".join(text_output)

    return all_text

# Generate embeddings using OpenAI
def generate_embedding(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]

# Store embeddings in PostgreSQL
def store_image_text_embeddings_in_postgres(main_folder='SachVan11'):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_text_embeddings (
        id SERIAL PRIMARY KEY,
        folder_name TEXT,
        embedding float8[]
    )
    """)
    conn.commit()

    # Process images and store embeddings
    all_text_data = extract_text_from_images(main_folder)
    for folder_name, text in all_text_data.items():
        if text:
            embedding = generate_embedding(text)
            cursor.execute(
                "INSERT INTO image_text_embeddings (folder_name, embedding) VALUES (%s, %s)",
                (folder_name, embedding)
            )
            conn.commit()
            print(f"Stored embedding for folder {folder_name}")

    cursor.close()
    conn.close()

# Call the function to store embeddings
store_image_text_embeddings_in_postgres()
