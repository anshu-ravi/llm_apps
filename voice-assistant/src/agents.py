from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, load_tools, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StdOutCallbackHandler



# A Simple AI Assistant that uses the ConversationChain to generate responses
# This agent doesn't have any memory or tools
class SimpleAIAssistant:
    def __init__(self, temperature=0.5, model_name='gpt-3.5-turbo') -> None:
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name, max_tokens=500)
        self.chain = ConversationChain(llm = self.llm)

    def run(self, text) -> str:
        response = self.chain.invoke(text)
        return response['response']
    

# An Advanced AI Assistant that uses the ConversationChain with memory and tools
# This agent has a memory and tools - google search 
class AdvancedAIAssistant:
    def __init__(self, temperature=0.5, model_name='gpt-3.5-turbo') -> None:
        self.memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name, max_tokens=250)
        self.tools = load_tools(['google-search'])
        self.agent = initialize_agent(agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, llm=self.llm, 
                                      memory=self.memory, tools=self.tools, verbose=False)
        # If you want to see the full chain, set verbose to True
        self.handler = StdOutCallbackHandler() 
    
    def run(self, text) -> str:
        response = self.agent.invoke(text, callbacks=[self.handler])
        print(type(response))
        return response['output']