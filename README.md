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




