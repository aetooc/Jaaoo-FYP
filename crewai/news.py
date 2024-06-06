import os
from serpapi import GoogleSearch

def GetNews(location):
    google_flights_key = os.environ.get("G_FLIGHTS_KEY")

    params = {
    "engine": "google_news",
    "q": location,
    "api_key": google_flights_key,
    # "topic_token": "Travel",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # print(results)
    news_results = results["news_results"][8:]

    titles_and_links = [{"title": news["title"], "link": news["link"]} for news in news_results]
    result = f"Top News in {location}:\n"
    # Displaying the extracted information
    for news in titles_and_links:
        result += (f'Title: {news["title"]}\nLink: {news["link"]}\n')
    
    print(result)
    return result
