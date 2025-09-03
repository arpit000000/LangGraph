import streamlit as st
from langgraph_back import chatbot
from langchain_core.messages import BaseMessage, HumanMessage
import uuid
#session state -> dict ek hoti hai jo bhi bhi reset nhoti isme record rkh skte hai unlike normal dict

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config = {'configurable':{'thread_id':thread_id}}).values['messages']


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


#side bar
st.sidebar.title('Langraph Chatbot by Arpit')

if st.sidebar.button('New Chat'):
    reset_chat()



st.sidebar.header('My Conversations') 
for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        temp_msg = []
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_msg.append({'role':role,'content':message.content})
        st.session_state['message_history'] = temp_msg

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

config = {'configurable':{'thread_id':st.session_state['thread_id']}}
user_input = st.chat_input('Type Here')
if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    with st.chat_message('assistant'):
        ai_msg = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=config,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_msg})
