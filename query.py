from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext, load_index_from_storage
from time import sleep

# Function to maintain a history of queries and responses
def maintain_history(history, query, response, max_history):
    history.append((query, response))
    # Ensure we only keep the last N items in history
    if len(history) > max_history:
        history.pop(0)
    return history

# Initial setup
print("Loading...")
sleep(1)
# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./storage")

# load index
index = load_index_from_storage(storage_context)
# documents = SimpleDirectoryReader("./markdown").load_data()
# service_context = ServiceContext.from_defaults(chunk_size=512)
# index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)
# index.storage_context.persist(persist_dir="./storage")
query_engine = index.as_query_engine()
print("Done!")

history = []  # Initialize an empty list to keep track of query history
max_history = 5  # Set how many recent queries you want to remember

# Main query loop
while True:
    query = input("Enter your query (or type 'exit' to quit): ")
    if query.lower() == 'exit':
        break  # Exit the loop if the user types 'exit'
    
    # full_query = "Chat History:\n\n"
    # import pdb; pdb.set_trace()
    # for h in history:
    #     full_query + "Q: " + h[0] + "\nA: " + h[1] + "\n\n"
    # full_query += "\n----\n\nQuery: \"" + query + "\" (Please quote code directory when relevant (According to...))"
    full_query = query + " (Please quote code directory when relevant (According to...))"

    response = query_engine.query(full_query)
    print("\n\n")
    print(response)
    
    # Update the history with the current query and response
    history = maintain_history(history, query, response.response, max_history)
    
    # Optionally, print the history (or you can do this upon a specific command)
    print("\nRecent Queries and Responses:")
    for q, r in history:
        print(f"Query: {q}\nResponse: {r}\n")
