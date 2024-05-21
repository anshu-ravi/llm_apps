# LLM Applications 

This repository contains various applications developed using Large Language Models (LLMs). Each folder within this repository represents a different application, showcasing the versatility and capabilities of LLMs in solving a wide range of tasks.

## Getting Started
To get started with any of the applications, you can clone the github repo, create a virtual environment, download the required libraries, navigate to the respective folder, and finally run the app. 

```
git clone https://github.com/anshu-ravi/llm_apps.git
cd llm_apps
conda create -n llm python==3.9 -y  
conda activate llm
pip install -r requirements.txt
```

After this, you need to create a `.env` file in the root folder and add the required API keys there. For example, this is how your file should look. In this was you can easily load your API keys in your python scripts while maintaining privacy and security.

```
OPENAI_API_KEY = <enter_your_key_here>
HUGGINGFACE_ACCESS_TOKEN = <enter_your_key_here>
```

Or you can also set its value using the environment variable from the terminal. To do this, run the following command 

```
export OPENAI_API_KEY='your-api-key'
```


## Applications

### Application 1: Blog Generator

Description

The Blog Generator app creates custom blog posts based on specified inputs such as topic, word limit, style, and target audience.


Features
1. Input: Users can specify the blog topic, word limit, writing style, and target audience.
2. Output: The app generates a tailored blog post meeting the specified criteria.
3. Technology Stack: Utilizes OpenAI's language model, LangChain for model orchestration, and Streamlit for the user interface.

This folder has 2 files:
- The `create_blog.py` has the function that sets up the prompt and does the API call to OpenAI. It then returns only the blog text.  
- The `app.py` is in charge of the setup for Streamlit.

To try the code on your local machine, run the following command and the streamlit sever should spin up on your local port.

```
streamlit run blog-generator/app.py
```


### Application 2: AI Voice Assistant 

The AI assistant is designed to interact with users through speech, leveraging OpenAI, SpeechRecognition, and Eleven Labs APIs to create a seamless conversational experience

Features
1. Speech Input: Captures and recognizes user speech using the SpeechRecognition library.
2. Natural Language Processing: Processes user input with GPT-3.5 Turbo via LangChain.
3. Conversational Memory: Maintains context across the conversation with ConversationBufferMemory.
4. Audio Response: Converts text responses to speech using the Eleven Labs library.
5. Continuous Interaction: Engages in a continuous conversation until the user says "quit" or "exit".

Key Components
1. SpeechRecognition: This library detects and captures audio input from the user, ensuring the assistant can listen and respond accurately.
2. LangChain Agent: A GPT-3.5 Turbo model acts as the language model, initialized with `CHAT_CONVERSATIONAL_REACT_DESCRIPTION` to handle conversational logic.
3. ConversationBufferMemory: This component allows the assistant to remember previous interactions, providing coherent and contextually appropriate responses.
4. Eleven Labs: This library converts text responses from the AI into natural-sounding audio output.

```
cd voice-assistant
conda activate llm
pip install -r requirements.txt
python3 app.py
```


For WSL users, you might have to install the following tools to use the libraries mentioned
```
sudo apt install portaudio19-dev # for input audio
sudo apt install ffmpeg # for output audio
```

### Application 3: Podcast Generator

This Podcast Generator is a web application that allows users to upload a PDF, select an audience type, and choose a language model (GPT-3.5 Turbo or GPT-4 Turbo) to generate a short, quick podcast. The application utilizes various AI and NLP tools to process the PDF, summarize its content, create a dialogue script, and convert the script to audio.

Features
1. PDF Upload: Users can upload a PDF document.
2. Audience Selection: Users can select the type of audience ('General', 'Technical', 'Beginner').
3. Model Selection: Users can choose between GPT-3.5 Turbo and GPT-4 Turbo for generating content.
4. Content Processing: The PDF is split into chunks and summarized using the map-reduce method.
5. Dialogue Generation: The summarized content is converted into a two-person dialogue script.
6. Audio Generation: The dialogue script is converted into audio using the Eleven Labs API.

How It Works?
1. PDF Processing: The uploaded PDF is read and split into manageable chunks using PyPDF2.
2. Content Summarization: 
    - The text chunks are summarized using the map-reduce method with Langchain and OpenAI models.
    - Custom prompts ensure the summaries are tailored to the selected audience.
3. Dialogue Generation:The summarized content is passed to another OpenAI model to generate a two-person dialogue script.
4. Audio Generation: The dialogue script is converted to audio using the Eleven Labs API.


```
cd podcast-generator
conda activate llm
pip install -r requirements.txt
python3 src/app.py
```