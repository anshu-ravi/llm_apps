import streamlit as st
from dotenv import load_dotenv
from writer import ScriptWriter
from voice import Voice # type: ignore

load_dotenv()

st.set_page_config(page_title="AI Podcaster 🎙️",  
                   layout="centered", 
                   initial_sidebar_state="expanded")
st.title('Create your own podcast in seconds! 🎙️🚀')

st.write('This app uses OpenAI to generate a quick podcast based on the document you provide. This offers a more fun and interesting way to learn new concepts')

# Get a file from the user 
uploaded_file = st.file_uploader("Choose a file", type=['pdf'])


input1_col, input2_col = st.columns(2)
with input1_col:
    AUDIENCE = st.selectbox('Select an audience type', ['General', 'Technical', 'Beginner'], index=0)

with input2_col:
    MODEL = st.selectbox('Select a model', ['gpt-3.5-turbo', 'gpt-4-turbo'], index=0)


generate_col, play_col = st.columns(2)
with generate_col:
    st.text("\n")
    # st.text("\n")
    submit = st.button("\n Generate Podcast! 🚀", use_container_width=True)


if uploaded_file is not None and submit:
    with st.spinner('Generating podcast...'):
        print(f"Generating podcast for {uploaded_file.name} with audience type {AUDIENCE}")
        sw = ScriptWriter(model_name=MODEL)
        script = sw.execute(uploaded_file, AUDIENCE)
        print('Script generated successfully!')
        voice_artist = Voice()
        audios = voice_artist.generate_audio(script)
        voice_artist.save_audio(audios)
    
    with play_col:
        st.text("\n")
        play = st.button("\n Play Podcast! 🎧", use_container_width=True)
    
    
    if play:
        st.success("Playing podcast...")
        voice_artist.play_audio(audios)
    
    st.success("Podcast generated successfully! 🎉🎙️")






    

