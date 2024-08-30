from flask import Flask, request, render_template, jsonify
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import XMLOutputParser
from functools import lru_cache
import psutil

app = Flask(__name__)

template = """Question: {question}

Answer: Analyze the question precisely and respond in a conversational style, without including explanations or analyses."""

llm = Ollama(model="phi3.5")

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

@lru_cache(maxsize=100)
def cached_generate_response(question):
    response = chain.invoke({"question": question})
    return response

def validate_question(question):
    if len(question) < 1 or len(question) > 300:
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.form.get('question', '')
    
    if not validate_question(question):
        return jsonify({'error': 'Invalid question length.'})
    
    try:
        response = cached_generate_response(question)
    except Exception as e:
        return jsonify({'error': f'An error occurred during processing: {str(e)}'}), 500
    
    return jsonify({'answer': response})

@app.route('/parse', methods=['POST'])
def parse():
    xml_data = request.data.decode('utf-8')

    if not xml_data:
        return jsonify({'error': 'No XML data provided.'}), 400
    
    if len(xml_data) > 1000:
        return jsonify({'error': 'XML data exceeds the maximum length of 1000 characters.'}), 400

    parser = XMLOutputParser()

    try:
        parsed_result = parser.parse(xml_data)
        response = cached_generate_response(parsed_result)
    except Exception as e:
        return jsonify({'error': f'An error occurred during XML parsing: {str(e)}'}), 500
    
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
