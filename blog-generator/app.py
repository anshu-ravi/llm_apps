## Streamlit App
import streamlit as st
from create_blog import get_openai_response

st.set_page_config(page_title="Blog Generator",  
                   layout="centered", 
                   initial_sidebar_state="expanded")
st.header('Blog Assistant Writer 🤖') 


topic =st.text_input("Enter the Blog Topic")
col1,col2 = st.columns(2)
with col1:
    n_words=st.text_input('Word Limit')
with col2:
    creative=st.selectbox('Creative Level', ['Low', 'Medium', 'High'])

col3,col4 = st.columns(2)
with col3:
    style=st.selectbox('Writing Style', ['Formal', 'Academic', 'Conversational'])
with col4:
    reader=st.selectbox('Reader Type', ['General', 'Technical', 'Beginner'])

submit=st.button("Generate")
if submit:
    response = get_openai_response(style, reader, topic, n_words, creative)
    st.write(response)


