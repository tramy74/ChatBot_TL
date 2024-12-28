# backend/app/indexing.py
from llama_index import LLMIndex
from database import get_connection  # Assuming you have a function to get DB connection

class DocumentIndexer:
    def __init__(self):
        self.connection = get_connection()
        self.index = LLMIndex(connection=self.connection)

    def index_documents(self, documents):
        for doc in documents:
            self.index.add_document(doc)
        self.index.build()

    def search(self, query):
        return self.index.search(query)

# Example usage
if __name__ == "__main__":
    indexer = DocumentIndexer()
    # Sample documents to index
    sample_docs = ["data"]
    indexer.index_documents(sample_docs)
