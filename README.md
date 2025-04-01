# **News Article Processing API**

This repo is the backend application for News Article summarization, labeling and keywords tagging. Powered by LLM.

## **Tech stack**
- `FastAPI` for making API
- `LangChain` for LLM interaction

## **Setup**
1. Create an `.env` file based on `.env.example` for Environment Variables
2. Run or deploy using `docker`

## **Run**
```sh
python main.py
```

## **Deploy**
```sh
docker build -t news-processing-api .
docker run -p <Forwarded Port>:<API Deployment Port> news-processing-api
```

## **API documentation**
| Endpoint           | Request Schema | Response Schema                                    | Description                                                   |
|--------------------|----------------|----------------------------------------------------|---------------------------------------------------------------|
| /summarize         | {"text": str}  | {"summary": str}                                   | Summary the content of the news article                       |
| /categorize        | {"text": str}  | {"category": str}                                  | Label the news article into one of the pre-defined categories |
| /extract_keywords  | {"text": str}  | {"keywords": str}                                  | Determine the tags of the news article                        |
| /process           | {"text": str}  | {"summary": str, "category": str, "keywords": str} | Summary, label and tag the news article in one call           |

| Error                 | Code | Description            |
|-----------------------|------|------------------------|
| Unprocessable Entity  | 422  | Invalid request format |
| Internal Server Error | 500  | An error happened      |

For more details, please access SwaggerUI at `http://<Host>:<API Deployment Port>/docs`

## Prompt Engineering Details
Below is the system prompt for the Summarization task:
```
You are a helpful AI assistant that helps the user to summarize news article content. You must analyze the given news content from the user, identify the main topic and idea to summary the news into a concise 3 sentences. Your output must contain a paragraph of exactly 3 sentences that represents the summary of the article without any explanation, as the user will parse the output directly into another module.
```

**Breakdown**
```
You are a helpful AI assistant that helps the user to summarize news article content.
```
This is to specify the goal of the AI, identify the role and the mission of it.


```
You must analyze the given news content from the user, identify the main topic and idea to summary the news into a concise 3 sentences
```
This part is to inform the AI of the input it has to deal with, the output it has to generate and give an instruction for it to complete the goal.


```
Your output must contain a paragraph of exactly 3 sentences that represents the summary of the article without any explanation, as the user will parse the output directly into another module.
```
This part is to encourage the AI to output only the result we need (3-sentence summarization)


All other system prompts is following the same strategy. For the Process task, I make a seperate system prompt instead of running 3 invocations for the subtasks, it will reduce the cost needed and since the AI is doing 3 subtasks that has a dependent relationship, it can receive more context and can help increase the quality of the output. 

---

Toka
