import psycopg2

# Kết nối lại với cơ sở dữ liệu PostgreSQL
connection = psycopg2.connect(
    dbname='chatbot_db', 
    user='postgres', 
    password='TRAmy_1960%', 
    host='localhost', 
    port='5432'
)

cursor = connection.cursor()

# Truy vấn để lấy dữ liệu embedding đã lưu
select_query = "SELECT * FROM vectors"
cursor.execute(select_query)
rows = cursor.fetchall()

# In kết quả
for row in rows:
    print(f"ID: {row[0]}, Title: {row[1]}, Embedding: {row[2]}")

cursor.close()
connection.close()
