import os
import warnings
import streamlit as st
from dotenv import load_dotenv
from transcript import get_transcript
from engine import VideoEngine


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
pc_api_key = os.getenv("PINECONE_API_KEY")

def start_chat(url: str) -> None:
    file_name = get_transcript(url)
    engine = VideoEngine(temperature=0.5, model_name="gpt-3.5-turbo")
    engine.create_chunks(file_name)
    st.session_state.engine = engine
    st.write("I have finished analyzing the video. You can now ask me any question about the video.")
    st.session_state.messages = []

def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.engine = None
    st.write("Chat history has been cleared. Please enter the Youtube link to start the chat")
    return None

def chat_input(prompt: str) -> None:
    if st.session_state.engine:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message('User'):
            st.markdown(prompt)
        
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            full_response = st.session_state.engine.answer_question(prompt)
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.write("Please enter the Youtube link to start the chat")

def main():
    st.title("Video Q&A Bot")
    st.write("This is a simple video Q&A bot that answers questions based on the context of the video \
             You can now ask all the silly and serious questions you have about the video! \
             Just enter the Youtube link and have fun!")
    
    # Initialize the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    url = st.text_input("Enter the Youtube link", key="url")
    col1, col2 = st.columns([1, 1])
    with col1:
        start = st.button("Start Chat", use_container_width=True)
    with col2:
        restart = st.button("Restart Chat", use_container_width=True)

    if restart:
        url = reset_chat()
        
    if url and start:
        start_chat(url)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input 
    if prompt := st.chat_input("Ask a question about the video"):
        chat_input(prompt)
        


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()




