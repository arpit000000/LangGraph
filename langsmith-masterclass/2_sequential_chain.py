from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['LANGCHAIN_PROJECT'] = 'seq_chain_demo'

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
model2 = model = ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite')

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

config = {'run_name':'Chain_seq',
    'tags':{'llm-app','report_generation','summarization'},
        'metadata':{'model1':'gemini-2.0-flash','model2':'gemini-2.0-flash-lite','model_temp':0.7}}

result = chain.invoke({'topic': 'Unemployment in India'},config=config)

print(result)
