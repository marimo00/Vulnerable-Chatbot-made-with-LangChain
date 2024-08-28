from flask import Flask, request, jsonify, render_template
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from functools import lru_cache
import xml.etree.ElementTree as ET  # XML 파서를 위한 모듈

# Flask를 사용하여 웹 애플리케이션을 생성
app = Flask(__name__)

# ChatPromptTemplate를 사용하여 대화의 템플릿을 정의
template = """Question: {question}

Answer: Analyze the question accurately and respond in no more than 3 lines, without including your analysis or any explanation in the answer."""

# 앱이 시작될 때 LLM 모델을 로드하여 미리 준비해둔다. 이는 실행 중에 모델을 빠르게 사용할 수 있게 해준다.
model = OllamaLLM(model="phi3.5")

# 정의한 템플릿을 사용하여 ChatPromptTemplate 객체를 생성
prompt = ChatPromptTemplate.from_template(template)

# 템플릿과 모델을 결합하여 대화 체인을 생성
chain = prompt | model

# LRU (Least Recently Used) 캐시 데코레이터를 사용하여 함수 결과를 캐싱
@lru_cache(maxsize=100)
def cached_generate_response(question):
    # 체인을 통해 모델에 질문을 던지고 응답을 받음
    response = chain.invoke({"question": question})
    return response

# XML 데이터를 파싱하는 함수
def parse_xml_question(xml_data):
    try:
        root = ET.fromstring(xml_data)
        question = root.find('question').text
        return question
    except ET.ParseError:
        return None

# 웹 애플리케이션의 기본 루트 경로 ('/')에 접속하면 'chatbot.html'을 렌더링하여 반환
@app.route('/')
def index():
    return render_template('chatbot.html')

# '/chat' 경로로 POST 요청이 들어오면 비동기적으로 질문에 대한 답변을 처리
@app.route('/chat', methods=['POST'])
async def chat():
    # 클라이언트로부터 전달된 XML 데이터를 추출
    xml_data = request.form.get('xml_data', '')
    if not xml_data:
        return jsonify({'error': 'No XML data provided.'})  # XML 데이터가 없으면 에러 메시지를 반환
    
    # XML 데이터를 파싱하여 질문을 추출
    question = parse_xml_question(xml_data)
    if not question:
        return jsonify({'error': 'Invalid XML format or missing <question> tag.'})  # XML 파싱 에러 시 반환
    
    # 비동기적으로 캐시된 응답을 호출 (비동기로 실행하기 위해 to_thread 사용)
    response = await asyncio.to_thread(cached_generate_response, question)
    
    # JSON 형식으로 응답을 반환
    return jsonify({'answer': response})

# 이 스크립트를 직접 실행할 때, Flask 앱을 디버그 모드에서 실행
if __name__ == '__main__':
    app.run(debug=True)
