import psycopg2

def create_table():
    conn = psycopg2.connect(
        dbname='chatbot_db', 
        user='postgres', 
        password='TRAmy_1960%', 
        host='localhost', 
        port='5432'
    )
    cursor = conn.cursor()

    # Tạo bảng books nếu nó chưa tồn tại
    create_table_query = """
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        content TEXT
    );
    """
    cursor.execute(create_table_query)

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    cursor.close()
    conn.close()

# Gọi hàm tạo bảng
create_table()

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def insert_book(title, content):
    conn = psycopg2.connect(
        dbname='chatbot_db', 
        user='postgres', 
        password='TRAmy_1960%', 
        host='localhost', 
        port='5432'
    )
    cursor = conn.cursor()
    
    # Chèn dữ liệu vào bảng
    insert_query = "INSERT INTO books (title, content) VALUES (%s, %s)"
    cursor.execute(insert_query, (title, content))

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    cursor.close()
    conn.close()

# Sử dụng
file_path = 'D:\\DaiHoc\\ForthYear\\chatbot\\backend\\data\\data.txt'  # Đường dẫn đến tệp văn bản
book_title = 'SachNguVan11T1'  # Tiêu đề cuốn sách
book_content = read_text_file(file_path)

insert_book(book_title, book_content)
