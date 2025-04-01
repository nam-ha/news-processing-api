import requests

# ==
def main():
    with open("dataset/test_news.txt", "r") as file:
        text = file.read()

    # # Summarize endpoint
    # try:
    #     response = requests.post(
    #         url = "http://localhost:8000/summarize",
    #         json = {
    #             "text": text
    #         }
    #     )
        
    #     response.raise_for_status()
        
    #     data = response.json()
    #     print(f"Summary: {data["summary"]}")
        
    # except requests.exceptions.RequestException as e:
    #     print(f"Error with the request: {e}")

    # # Categorize endpoint
    # try:
    #     response = requests.post(
    #         url = "http://localhost:8000/categorize",
    #         json = {
    #             "text": text
    #         }
    #     )
        
    #     response.raise_for_status()
        
    #     data = response.json()
    #     print(f"Category: {data["category"]}")
        
    # except requests.exceptions.RequestException as e:
    #     print(f"Error with the request: {e}")
    
    # # Extract Keywords endpoint
    # try:
    #     response = requests.post(
    #         url = "http://localhost:8000/extract_keywords",
    #         json = {
    #             "text": text
    #         }
    #     )
        
    #     response.raise_for_status()
        
    #     data = response.json()
    #     print(f"Keywords: {data["keywords"]}")
        
    # except requests.exceptions.RequestException as e:
    #     print(f"Error with the request: {e}")
    
    # Process endpoint
    try:
        response = requests.post(
            url = "http://localhost:8000/process",
            json = {
                "text": text
            }
        )
        
        response.raise_for_status()
        
        data = response.json()
        print(data)
        
    except requests.exceptions.RequestException as e:
        print(f"Error with the request: {e}")
        
if __name__ == "__main__":
    main()
