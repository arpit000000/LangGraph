from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
load_dotenv()
import sqlite3

config = {'configurable':{'thread_id':'thread-1'}}

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

conn = sqlite3.connect(database='chatbot.db',check_same_thread=False) 
#we put it as false bcoz it does not throw error it work on single thread and we use multithread


# Checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)
# res = chatbot.invoke(
#                 {'messages':[HumanMessage(content="what is My Name?")]},
#                 config=config)
# print(res)


#how many thread already used you check all by this it give unique and all as you write query
# all_thread = set()
# for vhe in checkpointer.list(None):
#     all_thread.add(vhe.config['configurable']['thread_id'])
# print(all_thread)

def retrieve_all_threads():
    all_thread = set()
    for vhe in checkpointer.list(None):
        all_thread.add(vhe.config['configurable']['thread_id'])
    return list(all_thread)