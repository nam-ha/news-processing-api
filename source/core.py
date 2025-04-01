import json

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# ==
class NewsAnalyzer():
    def __init__(self, backbone_model, backbone_model_provider):
        self._config_file = "configs/core.json"
        with open(self._config_file, "r") as file:
            self._config = json.load(file)
        
        self._backbone_model = backbone_model
        self._backbone_model_provider = backbone_model_provider
        
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
        
        is_completed = False
        num_retries = 0
        while not is_completed and num_retries <= 2:
            try:
                response = self._llm.invoke(prompt).content
                is_completed = True
                
            except Exception:
                num_retries += 1
        
        if is_completed:
            return response
        
        raise LLMRequestError(self._backbone_model, self._backbone_model_provider)

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
        
        is_completed = False
        num_retries = 0
        while not is_completed and num_retries <= 2:
            try:
                response = self._llm.invoke(prompt).content
                is_completed = True
                
            except Exception:
                num_retries += 1
        
        if is_completed:
            return response
        
        raise LLMRequestError(self._backbone_model, self._backbone_model_provider)
    
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
                
        is_completed = False
        num_retries = 0
        while not is_completed and num_retries <= 2:
            try:
                response = self._llm.invoke(prompt).content
                is_completed = True
                
            except Exception:
                num_retries += 1
        
        if is_completed:
            return response
                
        raise LLMRequestError(self._backbone_model, self._backbone_model_provider)
    
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
        
        is_completed = False
        num_retries = 0
        while not is_completed and num_retries <= 2:
            try:
                response = self._llm.invoke(prompt).content
                is_completed = True
                
            except Exception:
                num_retries += 1
        
        if is_completed:
            return response
                
        raise LLMRequestError(self._backbone_model, self._backbone_model_provider)

# ==
class NewsAnalyzerException(Exception):
    def __init__(self, message = "NewsAnalyzerException"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

class LLMRequestError(NewsAnalyzerException):
    def __init__(self, model, model_provider):
        self._model = model
        self._model_provider = model_provider
        
        self.message = f"LLMRequestError: An error occurred when trying to request to {model} of {model_provider}"
        super().__init__(self.message)

    def __str__(self):
        return self.message
