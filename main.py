from dotenv import load_dotenv
load_dotenv()

import os
import json
import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from source.core import NewsAnalyzer, NewsAnalyzerException

# ==
config_file = "configs/api.json"
with open(config_file, "r") as file:
    config = json.load(file)


# = Init modules =
analyzer = NewsAnalyzer(
    backbone_model = config['backbone_model'],
    backbone_model_provider = config['backbone_model_provider']
)


# = Define API =
app = FastAPI()

class NewsContent(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

class CategorizeResponse(BaseModel):
    category: str
    
class ExtractKeywordsResponse(BaseModel):
    keywords: str
    
@app.post("/summarize")
async def summarize(request_body: NewsContent) -> SummarizeResponse:
    try:
        summary = analyzer.summarize(
            text = request_body.text
        )
                
        return SummarizeResponse(
            summary = summary
        )
        
    except NewsAnalyzerException as nae:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(nae)}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(e)}"
        )

@app.post("/categorize")
async def categorize(request_body: NewsContent) -> CategorizeResponse:
    try:
        category = analyzer.categorize(
            text = request_body.text
        )
                
        return CategorizeResponse(
            category = category
        )
    
    except NewsAnalyzerException as nae:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(nae)}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(e)}"
        )
    
@app.post("/extract_keywords")
async def categorize(request_body: NewsContent) -> ExtractKeywordsResponse:
    try:
        keywords = analyzer.extract_keywords(
            text = request_body.text
        )
                
        return ExtractKeywordsResponse(
            keywords = keywords
        )
    
    except NewsAnalyzerException as nae:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(nae)}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(e)}"
        )

@app.post("/process")
async def process(request_body: NewsContent) -> JSONResponse:
    try:
        output = analyzer.process(
            text = request_body.text
        )
        
        return JSONResponse(
            content = output
        )

    except NewsAnalyzerException as nae:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(nae)}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Internal Server Error: {str(e)}"
        )
    
# == 
def main():
    uvicorn.run(
        app, 
        host = "0.0.0.0", 
        port = int(os.getenv('PORT'))
    )

if __name__ == '__main__':
    main()
