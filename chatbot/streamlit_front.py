import streamlit as st
from langgraph_back import chatbot
from langchain_core.messages import BaseMessage, HumanMessage

#session state -> dict ek hoti hai jo bhi bhi reset nhoti isme record rkh skte hai unlike normal dict

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

config = {'configurable':{'thread_id':'thread-1'}}
user_input = st.chat_input('Type Here')
if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)
    ai_msg = response['messages'][-1].content
    st.session_state['message_history'].append({'role':'assistant','content':ai_msg})
    with st.chat_message('assistant'):
        st.text(ai_msg)