from flask import Flask, request, jsonify, render_template
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Enhanced prompt template with detailed response structure
template = """Question: {question}

Answer: To provide a comprehensive answer, we will:
1. Break down the question into key components.
2. Analyze each part individually.
3. Combine insights to form a detailed response.

Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="phi3.5")

chain = prompt | model

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        question = request.form['question']
        response = chain.invoke({"question": question})
        answer = response.get('answer', 'No answer found.')
        return jsonify({'answer': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
