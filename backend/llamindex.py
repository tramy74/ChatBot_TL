import os
import sys
from dotenv import load_dotenv  # Import the library to load .env
from llama_index.llms.openai import OpenAI  # type: ignore
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from IPython.display import Markdown, display

# load documents
documents = SimpleDirectoryReader("data").load_data()

# set global settings config
llm = OpenAI(temperature=0, model="gpt-4o")
Settings.llm = llm
Settings.chunk_size = 512

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine(
    similarity_top_k=3,
    streaming=True,
)
response = query_engine.query(
    "Taylor Swift là ai?",
)

response.print_response_stream()


