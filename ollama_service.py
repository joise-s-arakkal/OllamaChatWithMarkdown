import sys
import json
import requests

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"

def stream_ollama_response(message):
    payload = {
        "messages": [{"role": "user", "content": message}],
        "model": "llama3.2",
        "stream": True
    }
    
    response = requests.post(OLLAMA_API_URL, json=payload, stream=True)

    if response.status_code != 200:
        print(json.dumps({"error": f"Error {response.status_code}"}))
        sys.stdout.flush()
        return
    
    buffer = ""
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            buffer += chunk
            lines = buffer.split("\n")
            for line in lines[:-1]:  # Process complete lines
                if line.strip() == "":
                    continue
                if line.startswith("data: "):
                    line = line[6:]  # Remove "data: " prefix
                try:
                    json_data = json.loads(line)
                    content = json_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    
                    formatted_content = content.encode("unicode_escape").decode("utf-8")

                    
                    print(json.dumps({"data": formatted_content}))
                    sys.stdout.flush()
                except json.JSONDecodeError:
                    break
            buffer = lines[-1]

if __name__ == "__main__":
    user_message = sys.argv[1] if len(sys.argv) > 1 else ""
    stream_ollama_response(user_message)
