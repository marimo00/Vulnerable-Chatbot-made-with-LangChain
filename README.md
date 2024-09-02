###### S-AI Training Project.

We made a Vulnerable Chatbot using LangChain.
CVE-2024-1455

#### Frmaework
langchain, python: flask

#### Modle
phi3.5

#### Production Plan
1. Create WarGame by implementing a chatbot with vulnerabilities.

2. Create a chatbot with LangChain. Chatbot is used by the chatbot (phi 3.5, limited to the class)

3. A chatbot is implemented using XML parser (results from LLM in the XML format) in LangChain.

4. Here, when using XML parser, a WarGame implementation that can obtain a Flag when attempting a billion laughs attack using code that could cause a billion laughs attack vulnerability.

#### Environmental Construction
1. Version - langchain 0.1.0, langchain-community 0.0.9, langchain-core 0.1.7, langsmith 0.0.77
2. Ollama Download curl -fsSL https://ollama.com/install.sh | sh
3. ollama pull phi3.5
* **Server** - Ubuntu LTS 20.4

#### Paylaods
[payload]https://huntr.com/bounties/4353571f-c70d-4bfd-ac08-3a89cecb45b6

use curl!!!

#### Attack Result
 ![AI2](https://github.com/user-attachments/assets/70ad7f5d-0c84-4b0c-a55f-0f5278133d48)
  **nice attack.**

  
 ![AI1](https://github.com/user-attachments/assets/05ff63f7-5d8a-4cc7-87a6-446bb27b8770)
 **If you got the result of the picture above, it is a version issue.**

 #### Reference
 [langchain github]https://github.com/langchain-ai/langchain/blob/v0.1.3/poetry.lock
 
 [CVE-2024-1455]https://data.safetycli.com/vulnerabilities/CVE-2024-1455/66962/
