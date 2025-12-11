import ollama
import time

print("Testing Ollama Connectivity...")
start = time.time()
try:
    response = ollama.chat(model='llama3', messages=[
      {'role': 'user', 'content': 'Hello, are you working? Reply with one word.'},
    ])
    print("Response:", response['message']['content'])
    print(f"Time taken: {time.time() - start:.2f}s")
except Exception as e:
    print(f"Error: {e}")
