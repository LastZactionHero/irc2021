from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext, load_index_from_storage
from time import sleep
import os

def maintain_history(history, query, response, max_history):
    history.append((query, response))
    if len(history) > max_history:
        history.pop(0)
    return history


print("Loading... may take a few minutes...")
index = None
if os.path.exists("./storage/docstore.json"):
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader("./markdown").load_data()
    service_context = ServiceContext.from_defaults(chunk_size=512)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)
    index.storage_context.persist(persist_dir="./storage")
query_engine = index.as_query_engine()


history = []
max_history = 5

while True:
    query = input("Enter your query (or type 'exit' to quit, or 'clear' to clear history): ")
    if query.lower() == 'exit':
        break
    if query.lower() == 'clear':
        history = []
        continue
    
    merged_history = "Previous Conversation: \n" if len(history) > 0 else ""
    for q, r in history:
        merged_history += f"Query: {q}\nResponse: {r}\n\n"
    merged_history += "\n\n----\n\n" if len(history) > 0 else ""

    full_query = merged_history + "Query: " + query
    response = query_engine.query(full_query)
    print("\n\n")
    print(response)

    print("Passages:")
    for source_node in response.source_nodes:
        # code_section = response.source_nodes[0].metadata['file_name'].split("_")[1].split(".")[0]
        print(source_node.text)
        print("\n")


    history = maintain_history(history, query, response.response, max_history)
