import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt

# ✅ Must be the first command
st.set_page_config(page_title="Medical Chatbot", layout="wide")

# Load environment variables
load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["GROQ_API_KEY"] = GROQ_API_KEY

PINECONE_API_KEY="pcsk_3P8KL7_TrBnWA3L97ZhYzvRpiUdRizaWraHvXN7mbaVKxnvbgRHE1H2Ufne3ZHyx7NmrLP"
GROQ_API_KEY = "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"

# ✅ Cache embeddings to prevent reloading on every interaction (silent loading)
@st.cache_resource
def load_embeddings():
    return download_hugging_face_embeddings()

# ✅ Cache Pinecone retriever (silent loading)
@st.cache_resource
def load_retriever():
    embeddings = load_embeddings()
    index_name = "medicalbot"
    docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
    return docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# ✅ Cache LLM model (silent loading)
@st.cache_resource
def load_llm():
    return ChatGroq(
        temperature=0.4,
        max_tokens=500,
        model_name="llama-3.3-70b-versatile"
    )

# ✅ Track initialization state
if "initialized" not in st.session_state:
    st.session_state["retriever"] = load_retriever()
    st.session_state["llm"] = load_llm()
    st.session_state["initialized"] = True

# # Ensure history file exists
# HISTORY_FILE = "history.csv"
# if not os.path.exists(HISTORY_FILE):
#     pd.DataFrame(columns=["User Input", "Chatbot Response"]).to_csv(HISTORY_FILE, index=False)

# Create RAG chain
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(st.session_state["llm"], prompt)
rag_chain = create_retrieval_chain(st.session_state["retriever"], question_answer_chain)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Chat", "About"])

if page == "Chat":
    st.title("🩺 Medical Chatbot")
    st.write("Ask me anything about health!")

    # Initialize chat messages in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display chat history
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Thinking..."):
            response = rag_chain.invoke({"input": user_input})
            bot_response = response["answer"]

        st.session_state["messages"].append({"role": "assistant", "content": bot_response})
        
        with st.chat_message("assistant"):
            st.markdown(bot_response)

        # # ✅ Save conversation history
        # history = pd.read_csv(HISTORY_FILE)
        # new_entry = pd.DataFrame([[user_input, bot_response]], columns=["User Input", "Chatbot Response"])
        # history = pd.concat([history, new_entry], ignore_index=True)
        # history.to_csv(HISTORY_FILE, index=False)

# elif page == "History":
#     st.title("📜 Chat History")
    
#     try:
#         history = pd.read_csv(HISTORY_FILE)
        
#         if history.empty:
#             st.write("No chat history available.")
#         else:
#             # Display each past chat in a chat-style format
#             for index, row in history.iterrows():
#                 with st.chat_message("user"):
#                     st.markdown(f"**You:** {row['User Input']}")
#                 with st.chat_message("assistant"):
#                     st.markdown(f"**Chatbot:** {row['Chatbot Response']}")
#     except Exception as e:
#         st.write("Error loading history:", e)


elif page == "About":
    st.title("ℹ️ About the Medical Chatbot")
    
    st.markdown("""
    ## Overview  
    The **Medical Chatbot** is an AI-powered virtual assistant designed to provide instant responses to health-related inquiries.  
    By leveraging state-of-the-art **Natural Language Processing (NLP)** and **Retrieval-Augmented Generation (RAG)**,  
    this chatbot enhances accessibility to medical information while maintaining an interactive and user-friendly experience.

    ## Technology Stack  
    The chatbot is built using cutting-edge AI frameworks and cloud-based vector search engines:  
    - **Language Model:** Groq’s **LLama-3.3-70B Versatile**  
    - **Retrieval System:** Pinecone **Vector Database** for document storage and similarity search  
    - **Frameworks:** **LangChain** for AI-driven response generation  
    - **Frontend:** **Streamlit** for an intuitive and interactive user experience  

    ## Features  
    🔹 **Intelligent Health Query Resolution** – Retrieves and generates relevant medical insights.  
    🔹 **Conversational Memory** – Stores chat history for reference.  
    🔹 **Efficient Search Mechanism** – Utilizes embeddings for similarity-based document retrieval.  
    🔹 **Secure & Scalable** – Built with **Pinecone** and **Groq LLM** to handle large-scale queries.  

    ## How It Works  
    1. **User Query Processing:** The chatbot receives a user's health-related question.  
    2. **Retrieval Mechanism:** Relevant medical documents are retrieved using **Pinecone Vector Store**.  
    3. **AI-Powered Response:** The chatbot generates responses by combining retrieved knowledge with **LLM-based inference**.  
    4. **Interactive Experience:** Users receive instant and contextually accurate answers.  

    ## Disclaimer  
    ⚠️ **This chatbot is intended for informational purposes only.** It does not provide professional medical advice, diagnosis, or treatment.  
    Always consult a qualified healthcare provider for medical concerns.  

    ---  

    ## Developer Contact  
    👩‍💻 **Developed by Ananya Krishna**  
    📧 Email: [ananyakrish124@gmail.com](mailto:ananyakrish124@gmail.com)  
    🔗 GitHub: [github.com/ananyakrishnaeemani](https://github.com/ananyakrishnaeemani)  
    🔗 LinkedIn: [linkedin.com/in/ananyakrishna](https://www.linkedin.com/in/ananyakrishna/)  
    """)
