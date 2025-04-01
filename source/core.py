import json

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# ==
class NewsAnalyzer():
    def __init__(self, backbone_model, backbone_model_provider):
        self._config_file = "configs/core.json"
        with open(self._config_file, "r") as file:
            self._config = json.load(file)
            
        self._llm = init_chat_model(
            model = backbone_model, 
            model_provider = backbone_model_provider
        )
        
    def summarize(self, text):            
        system_template = self._config['summarization']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "text": text
            }
        )
        
        response = self._llm.invoke(prompt).content
        
        return response

    def categorize(self, text):
        system_template = self._config['categorization']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "categories": self._config['categorization']['categories'],
                "text": text
            }
        )
        
        response = self._llm.invoke(prompt).content
        
        return response
    
    def extract_keywords(self, text):
        system_template = self._config['keywords_extraction']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "text": text
            }
        )
        
        response = self._llm.invoke(prompt).content
        
        try:
            keywords = json.loads(response)
            
        except Exception as e:
            #TODO: Handle retry
            pass
        
        return response
    
    def process(self, text):
        system_template = self._config['processing']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "categories": self._config['processing']['categories'],
                "text": text
            }
        )
        
        response = self._llm.invoke(prompt).content
                
        return response
