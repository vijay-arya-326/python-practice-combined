import requests
from langchain_core.tools import tool

@tool
def searxng_web_search(searchStr: str):
    """Search web and provide results"""
    searchUrl = "http://localhost:8080/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    params = {
        "q": searchStr,
        "format": "json"
    }

    response = requests.get(searchUrl, params=params, headers=headers)

    extracted_data = []
    for item in response.json()["results"]:
        extracted_data.append(
            {
                "url": item.get("url"),
                "title": item.get("title"),
                "content": item.get("content")
            }
        )

    return extracted_data


if __name__ == "__main__":
    list1 = searxng_web_search.invoke({"searchStr": "playwright"})
    list2 = searxng_web_search.invoke({"searchStr": "intellij"})

    finalList = list1 + list2

    for item in finalList:
        print(f"""{item["url"]} --> {item["title"]}""")




