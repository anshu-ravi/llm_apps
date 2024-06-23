import os
import pinecone 

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.prompts import ChatPromptTemplate


pc_api_key = os.getenv("PINECONE_API_KEY")

class VideoEngine:
    def __init__(self, temperature: float, model_name:str) -> None:
        self.pc = pinecone.Pinecone(api_key=pc_api_key)
        self.project_name = "rags-with-video"
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name)
        self.parser = StrOutputParser()

    def create_chunks(self, file_name: str) -> None:
            """
            Creates chunks from a given file.

            Args:
                file_name (str): The name of the file to create chunks from.

            Returns:
                None
            """
            
            # Load the text from the file using the TextLoader
            loader = TextLoader(file_name) 
            text_documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=25)
            documents = splitter.split_documents(text_documents)

            # Create a Pinecone index from the documents and embeddings so that it can be used for quick inference retrieval
            self.db = Pinecone.from_documents(documents, self.embeddings, 
                                              index_name=self.project_name)
    
    def answer_question(self, question: str) -> str:
            """
            Answers the given question based on the provided context.

            Args:
                question (str): The question to be answered by the LLM.

            Returns:
                str: The answer to the question.

            Raises:
                None

            Example:
                >>> engine = Engine()
                >>> context = "Patricia likes white cars"
                >>> question = "What color is Patricia's car?"
                >>> engine.answer_question(question)
                'White'
            """
            
            template = """
            Answer the question based on the context below. 
            Make sure the answer is not too short, has all the relevant information, and is factually correct.
            Replying with a single word or a short phrase is not sufficient.
            If you can't answer the question, reply "I don't know".

            Context: {context}

            Question: {question}
            """

            prompt = ChatPromptTemplate.from_template(template)
            setup = RunnableParallel(context = self.db.as_retriever(), question = RunnablePassthrough())
            chain = setup | prompt | self.llm | self.parser
            answer = chain.invoke(question)

            return answer
