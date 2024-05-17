import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
hf_key = os.getenv("HUGGINGFACE_ACCESS_TOKEN")
MODEL = 'gpt-3.5-turbo'


def get_openai_response(style, reader, topic, word_limit, creative):
    template = """
        Write a blog post in the style of {style}, intended for {reader}, on the topic of {topic} 
        within {word_limit}. Make sure the content is engaging and informative
    """

    prompt = PromptTemplate(
    input_variables=["style", "reader", "topic", 'word_limit'],
    template=template,
    )   

    if creative.lower() == 'high':
        temperature = 0.9
    elif creative.lower() == 'medium':
        temperature = 0.45
    else:
        temperature = 0.2

    llm = ChatOpenAI(temperature=temperature, model_name=MODEL)

    chain = prompt | llm

    blog_post = chain.invoke({
    "style": style,
    "reader": reader,
    "topic": topic, 
    'word_limit': word_limit
    })

    return blog_post.content
