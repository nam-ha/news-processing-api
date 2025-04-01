import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from source.core import NewsAnalyzer

# ==
def main():
    analyzer = NewsAnalyzer(
        backbone_model = "gpt-4o-mini",
        backbone_model_provider = "openai"
    )
    
    with open("dataset/test_news.txt", "r") as file:
        news_content = file.read()
            
    summary = analyzer.summarize(news_content)
    category = analyzer.categorize(news_content)
    keywords = analyzer.extract_keywords(news_content)
    
    print(f"==\n{news_content}\n==\nSummary: {summary}\nCategory: {category}\nKeywords: {keywords}\n==")
    
    
if __name__ == "__main__":
    main()
