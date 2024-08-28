from flask import Flask, request, jsonify, render_template
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from functools import lru_cache
import re
import xml.etree.ElementTree as ET

app = Flask(__name__)

template = """Question: {question}

Answer: Analyze the question precisely and respond in a conversational style, without including explanations or analyses."""

model = OllamaLLM(model="phi3.5")

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

@lru_cache(maxsize=100)
def cached_generate_response(question):
    response = chain.invoke({"question": question})
    return response

@app.route('/')
def index():
    return render_template('chatbot.html')

def validate_question(question):
    if len(question) < 1 or len(question) > 300:
        return False
    return True

@app.route('/chat', methods=['POST'])
async def chat():
    question = request.form.get('question', '')
    
    if not validate_question(question):
        return jsonify({'error': 'Invalid question format or length.'})
    
    response = await asyncio.to_thread(cached_generate_response, question)
    
    return jsonify({'answer': response})

@app.route('/parse_xml', methods=['POST'])
async def parse_xml_route():
    xml_content = request.form.get('xml_content', '')
    
    if not xml_content:
        return jsonify({'error': 'No XML content provided'})
    
    try:
        root = ET.fromstring(xml_content)
        parsed_data = {elem.tag: elem.text for elem in root.iter()}
    except ET.ParseError as e:
        return jsonify({'error': 'Invalid XML format'})
    
    return jsonify({'parsed_data': parsed_data})

if __name__ == '__main__':
    app.run(debug=False)