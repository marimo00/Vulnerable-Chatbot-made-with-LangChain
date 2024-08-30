function appendMessage(text, sender) {
    const chatbox = document.getElementById('chatbox');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = text;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function toggleInputState(disabled) {
    const questionInput = document.getElementById('question');
    const sendButton = document.getElementById('sendButton');
    questionInput.disabled = disabled;
    sendButton.disabled = disabled;
}

function handleError(error) {
    appendMessage('An error occurred: ' + error.message, 'bot');
}

function sendMessage() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();
    if (question) {
        appendMessage(question, 'user');
        questionInput.value = '';
        toggleInputState(true);

        const loadingMessage = document.createElement('div');
        loadingMessage.classList.add('message', 'bot', 'loading');
        loadingMessage.textContent = 'Generating answer...';
        document.getElementById('chatbox').appendChild(loadingMessage);
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'question': question
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            loadingMessage.remove();
            if (data.answer) {
                appendMessage(data.answer, 'bot');
            } else if (data.error) {
                appendMessage('error: ' + data.error, 'bot');
            }
        })
        .catch(error => {
            loadingMessage.remove();
            handleError(error);
        })
        .finally(() => {
            toggleInputState(false);
        });
    }
}

document.getElementById('question').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById('sendButton').addEventListener('click', sendMessage);
