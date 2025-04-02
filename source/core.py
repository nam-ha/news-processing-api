import json

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

# ==
def format_keywords_str(keywords_str, max_num_keywords):
    keywords = keywords_str.split(', ')
    
    list_formatted_keywords_str = str(keywords[:max_num_keywords])
        
    return list_formatted_keywords_str

def format_process_output(process_output, max_num_keywords):
    mark1 = process_output.find('Summary')
    mark2 = process_output.find('Category')
    mark3 = process_output.find('Tags')
    
    summary = process_output[mark1 + 9:mark2 - 1].strip()
    category = process_output[mark2 + 10:mark3 - 1].strip()
    keywords_str = process_output[mark3 + 10:].strip()
    
    keywords = format_keywords_str(keywords_str, max_num_keywords)
    
    return summary, category, keywords

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
    
    def _request_llm(self, prompt, max_num_retries = 2):
        is_completed = False
        num_retries = 0
        while not is_completed and num_retries <= max_num_retries:
            try:
                response = self._llm.invoke(prompt).content
                is_completed = True
                
            except Exception as e:
                num_retries += 1
                print(f"An error happened when trying to request to the provider: {e}. Retrying ... ({num_retries}/{max_num_retries})")
                
        if is_completed:
            return response
        
        raise LLMRequestError(self._backbone_model, self._backbone_model_provider)
    
    def summarize(self, text):            
        system_template = self._config['summarization']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "text": text,
                
                "num_summary_sentences": self._config['summarization']['num_summary_sentences']
            }
        )
        
        response = self._request_llm(prompt)
        
        return response

    def categorize(self, text):
        system_template = self._config['categorization']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "text": text,
                
                "categories": self._config['categorization']['categories']
            }
        )
        
        response = self._request_llm(prompt)
        
        return response
    
    def extract_keywords(self, text):
        system_template = self._config['keywords_extraction']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "text": text,
                
                "min_num_keywords": self._config['keywords_extraction']['min_num_keywords'],
            }
        )
        breakpoint()
        response = self._request_llm(prompt)
        breakpoint()
        keywords = format_keywords_str(response, self._config['keywords_extraction']['max_num_keywords'])
        
        return keywords
    
    def process(self, text):
        system_template = self._config['processing']['system_template']
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        
        prompt = prompt_template.invoke(
            {
                "text": text,
                
                "num_summary_sentences": self._config['processing']['num_summary_sentences'],
                "categories": self._config['processing']['categories'],
                "min_num_keywords": self._config['processing']['min_num_keywords'],
            }
        )
        
        response = self._request_llm(prompt)
        breakpoint()
        summary, category, keywords = format_process_output(response, self._config['processing']['max_num_keywords'])
        
        return {
            "summary": summary,
            "category": category,
            "keywords": keywords
        }

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
