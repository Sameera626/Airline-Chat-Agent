from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

file_response = client.files.create(
    file = open("airline_policies.pdf", "rb"),
    purpose = "assistants"
)

file_id = file_response.id
print(f"Uploaded file ID: {file_id}")

vector_store_response = client.vector_stores.create(
    name="My FAQ Vector Store"
)

vector_store_id = vector_store_response.id
print(f"Created vector store ID: {vector_store_id}")

client.vector_stores.files.create(
    vector_store_id = vector_store_id,
    file_id = file_id
)
print("File attached to vector store.")

print(f"Use this vector_store_id in your tool config: {vector_store_id}")