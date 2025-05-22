from flask import Flask, render_template, request, Response
import subprocess
import json

app = Flask(__name__)

def stream_ollama_response(message):
    process = subprocess.Popen(
        ["python", "ollama_service.py", message],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            try:
                json_data = json.loads(output.strip())
                content = json_data.get("data", "")
                yield f"data: {content}\n\n"
            except json.JSONDecodeError:
                continue

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET'])
def chat():
    user_input = request.args.get("message")
    return Response(stream_ollama_response(user_input), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5001,host="0.0.0.0")
