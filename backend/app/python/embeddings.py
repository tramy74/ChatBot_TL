from sentence_transformers import SentenceTransformer
import numpy as np

# Khởi tạo mô hình
model = SentenceTransformer('all-MiniLM-L6-v2')

def text_to_vector(text):
    vector = model.encode(text)
    return vector

import psycopg2

# Kết nối tới cơ sở dữ liệu PostgreSQL
connection = psycopg2.connect(
    dbname='chatbot', 
    user='postgres', 
    password='TRAmy_1960%', 
    host='localhost', 
    port='5432'
)

cursor = connection.cursor()

def save_vector_to_db(vector, text_id, title):
    vector_list = vector.tolist()  # Chuyển numpy array thành list
    insert_query = "INSERT INTO vectors (id, title, vector) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (text_id, title, vector_list))
    connection.commit()


# Ví dụ sử dụng
text_file_path = 'D:/DaiHoc/ForthYear/chatbot/backend/data/data.txt'
with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()
    vector = text_to_vector(text)
    save_vector_to_db(vector, text_id=1, title='Sample Title')  # Thêm tiêu đề phù hợp


cursor.close()
connection.close()
