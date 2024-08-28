from flask import Flask, request, jsonify, render_template, g
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import XMLOutputParser
import time
from functools import lru_cache

app = Flask(__name__)

template = """Question: {question}

Answer: Analyze the question precisely and respond in a conversational style, without including explanations or analyses."""

model = OllamaLLM(model="phi3.5")

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

request_count = {}
BLOCK_DURATION = 60
THRESHOLD = 100

@lru_cache(maxsize=100)
def cached_generate_response(question):
    response = chain.invoke({"question": question})
    return response

def validate_question(question):
    if len(question) < 1 or len(question) > 300:
        return False
    return True

def detect_dos():
    ip = request.remote_addr
    current_time = time.time()
    
    if ip not in request_count:
        request_count[ip] = []
    
    request_count[ip] = [timestamp for timestamp in request_count[ip] if current_time - timestamp < 60]
    
    request_count[ip].append(current_time)
    
    if len(request_count[ip]) > THRESHOLD:
        g.attack = True
        g.attack_flag = "XML_B000000MB_B000000MB" 
        return True
    
    g.attack = False
    return False

@app.before_request
def before_request():
    if detect_dos():
        print(f"Potential DoS attack detected from IP: {request.remote_addr}")

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    if g.get('attack', False):
        return jsonify({'error': g.get('attack_flag')}), 429
    
    question = request.form.get('question', '')
    
    if not validate_question(question):
        return jsonify({'error': 'Invalid question format or length.'})
    
    response = cached_generate_response(question)
    
    return jsonify({'answer': response})

@app.route('/parse_xml', methods=['POST'])
def parse_xml_route():
    if g.get('attack', False):
        return jsonify({'error': g.get('attack_flag')}), 429

    xml_content = request.form.get('xml_content', '')
    
    if not xml_content:
        return jsonify({'error': 'No XML content provided'})
    
    try:
        parser = XMLOutputParser()
        parsed_data = parser.parse(xml_content)
    except Exception as e:
        return jsonify({'error': 'Invalid XML format'})
    
    return jsonify({'parsed_data': parsed_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
