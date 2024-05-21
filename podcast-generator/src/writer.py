from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from PyPDF2 import PdfReader
import os



class ScriptWriter():
    def __init__(self, model_name):
        self.llm = ChatOpenAI(temperature=0.5, max_tokens=700, model=model_name)
        self.chunk_size = 12000
        self.overlap = 50


    def load_pdf(self, file_path):
        save_path = file_path.name.split('.')[0]
        os.makedirs('data', exist_ok=True)
        with open(f"data/{save_path}", "wb") as f:
            f.write(file_path.read())
        
        pdfreader = PdfReader(save_path)
        
        # Read text from the pdf 
        text = ''
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                text += content
        return text
    
    def chunk_text(self, text, chunk_size, overlap):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        chunks = splitter.create_documents([text])
        return chunks 
    
    def generate_summary(self, chunks):
        # Summarization chain
        summary_prompt = """You are an expert in the field of meta-learning. 
        You are provided with a text. 
        You need to extract the key points from the text. 
        The points should be helpful in creating a script for a podcast episode.

        TEXT: {text}

        Key points:"""
        map_prompt_template = PromptTemplate(input_variables=["text"],
                                        template=summary_prompt,)
        
        
        # Combining all the summaries together 
        combine_prompt = """Provide a final summary of the entire document with these key points 
        The overall summary should be helpful in creating a script for a podcast episode.
        When dealing with scientific topics, mention the data as well.

        Key points: {key_points}"""

        reduce_prompt_template = PromptTemplate(input_variables=["key_points"],
                                        template=combine_prompt,)
        
        summary_chain = load_summarize_chain(
            llm = self.llm, 
            chain_type="map_reduce",
            map_prompt=map_prompt_template,
            map_reduce_document_variable_name="text",
            combine_prompt=reduce_prompt_template,
            combine_document_variable_name="key_points",
            verbose=False
        )

        output = summary_chain.invoke(chunks)
        return output
    
    def write_script(self, summary, AUDIENCE):
        #Podcast chain 
        podcast_writer = """
        System: You are an expert scriptwriter. You are provided with a summary of a document.
        You need to create a coherent and engaging script for a podcast episode based on this summary.
        Make it a conversation between two hosts.
        Remember, the podcast is for a {AUDIENCE} audience. 
        There should at least be 10 dialogues from each person. Make it detailed and as a conversation
        Please follow the structure below for the script for a 2 min episode.:

        Summary: {summary}

        Podcast Script:
        Person 1: 
        Person 2:

        """ 

        writer_prompt = PromptTemplate(input_variables=["AUDIENCE", "summary"],
                                        template=podcast_writer)
        writer_chain = writer_prompt | self.llm
        final_response = writer_chain.invoke({"AUDIENCE": AUDIENCE, 
                                      "summary": summary['output_text']})
        return final_response
    

    def execute(self, filepath, AUDIENCE):
        text = self.load_pdf(filepath)
        print('Sucessfully loaded the pdf')

        chunks = self.chunk_text(text, self.chunk_size, self.overlap)
        print('Sucessfully chunked the text')
        summary = self.generate_summary(chunks)
        print('Sucessfully generated the summary')
        script = self.write_script(summary, AUDIENCE)
        
        return script


        
        