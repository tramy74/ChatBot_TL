from database_setup import create_tables
from backend.app.llamaindex import embed_texts

if __name__ == "__main__":
    # Tạo bảng trong cơ sở dữ liệu
    create_tables()

    # Đường dẫn đến thư mục chứa file TXT
    data_folder = 'data'  # Thay đổi đường dẫn nếu cần

    # Thêm embeddings vào bảng
    embed_texts(data_folder)
