from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDocumentStore

from dotenv import load_dotenv
import os
import openai
import psycopg2

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def embed_text(file_path):
    # Đọc nội dung từ tệp
    text = read_text_file(file_path)

    # Tạo Document từ nội dung (có thể sử dụng SimpleDocument)
    doc = SimpleDocumentStore(text=text)  # Hoặc một lớp tương đương khác nếu có

    # Khởi tạo VectorStoreIndex với Document
    index = VectorStoreIndex([doc])  # Sử dụng doc ở đây
    vectors = index.get_vectors()  # Lấy vector cho document

    return vectors

def insert_vector(title, vector):
    conn = psycopg2.connect(
        dbname='chatbot', 
        user='postgres', 
        password='TRAmy_1960%', 
        host='localhost', 
        port='5432'
    )
    cursor = conn.cursor()
    
    # Chèn dữ liệu vào bảng vectors (giả sử bạn đã tạo bảng này)
    insert_query = "INSERT INTO vectors (title, vector) VALUES (%s, %s)"
    cursor.execute(insert_query, (title, vector))

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    cursor.close()
    conn.close()

# Sử dụng
file_path = 'D:\\DaiHoc\\ForthYear\\chatbot\\backend\\data\\data.txt'  # Đường dẫn đến tệp văn bản
book_title = 'SachNguVan11T1'  # Tiêu đề cuốn sách
vector = embed_text(file_path)  # Tạo vector từ tệp văn bản
insert_vector(book_title, vector)  # Chèn vector vào cơ sở dữ liệu

print("Vector đã được chèn vào cơ sở dữ liệu thành công!")
