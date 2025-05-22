function sendMessage() {
            const userInput = document.getElementById("user-input").value;
            document.getElementById("user-input").value = "";
            const chatBox = document.getElementById("chat-box");
            chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

            const botDivId = `bot-${Date.now()}`;
            chatBox.innerHTML += `<div id="${botDivId}"><strong>Bot:</strong><div class="bot-message"><pre><code></code></pre></div></div>`;

            let markdownBuffer = "";

            const eventSource = new EventSource(`/chat?message=${encodeURIComponent(userInput)}`);
            eventSource.onmessage = function(event) {
                markdownBuffer += event.data;

                // Convert visible \n and \t back to actual characters
                let parsedMarkdown = markdownBuffer
                    .replace(/\\n/g, "\n")
                    .replace(/\\t/g, "\t");

                const html = marked.parse(parsedMarkdown);
                document.querySelector(`#${botDivId} .bot-message`).innerHTML = html;
                hljs.highlightAll();
            };

            eventSource.onerror = function() {
                eventSource.close();
            };
        }