from openai import OpenAI
client = OpenAI()

with open(
    "D:\\DaiHoc\\ForthYear\\chatbot\\backend\\data\\data.txt", 
    "r", 
    encoding="utf-8") as f:
    text_content = f.read()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input=text_content
)

embeddings = response.data[0].embedding
# Process the embeddings as needed (e.g., store them, calculate distances)
print(response)