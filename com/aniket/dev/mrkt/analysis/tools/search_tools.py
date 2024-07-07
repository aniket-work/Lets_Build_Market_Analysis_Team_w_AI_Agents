import json
import os
import requests
from langchain.tools import tool


class SearchTools():
    # Constants
    TOP_RESULTS       = 4
    SEARCH_URL        = "https://google.serper.dev/search"
    NEWS_URL          = "https://google.serper.dev/news"
    CONTENT_TYPE      = 'application/json'
    API_KEY_ENV       = 'SERPER_API_KEY'
    TITLE_PREFIX      = "Title: "
    LINK_PREFIX       = "Link: "
    SNIPPET_PREFIX    = "Snippet: "
    SEPARATOR         = "\n-----------------"
    HEADER_X_API_KEY  = 'X-API-KEY'

    HEADER_CONTENT_TYPE = 'content-type'
    ORGANIC_KEY         = 'organic'
    NEWS_KEY            = 'news'
    TITLE_KEY           = 'title'
    LINK_KEY            = 'link'
    SNIPPET_KEY         = 'snippet'

    TOOL_SEARCH_INTERNET = "Search the internet"
    TOOL_SEARCH_NEWS     = "Search news on the internet"

    @tool(TOOL_SEARCH_INTERNET)
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant results"""
        payload = json.dumps({"q": query})
        headers = {
            SearchTools.HEADER_X_API_KEY: os.environ[SearchTools.API_KEY_ENV],
            SearchTools.HEADER_CONTENT_TYPE: SearchTools.CONTENT_TYPE
        }
        response = requests.request("POST", SearchTools.SEARCH_URL, headers=headers, data=payload)
        results = response.json()[SearchTools.ORGANIC_KEY]
        return SearchTools._format_results(results)

    @tool(TOOL_SEARCH_NEWS)
    def search_news(query):
        """Useful to search news about a company, stock or any other topic and return relevant results"""
        payload = json.dumps({"q": query})
        headers = {
            SearchTools.HEADER_X_API_KEY: os.environ[SearchTools.API_KEY_ENV],
            SearchTools.HEADER_CONTENT_TYPE: SearchTools.CONTENT_TYPE
        }
        response = requests.request("POST", SearchTools.NEWS_URL, headers=headers, data=payload)
        results = response.json()[SearchTools.NEWS_KEY]
        return SearchTools._format_results(results)

    @staticmethod
    def _format_results(results):
        string = []
        for result in results[:SearchTools.TOP_RESULTS]:
            try:
                string.append('\n'.join([
                    f"{SearchTools.TITLE_PREFIX}{result[SearchTools.TITLE_KEY]}",
                    f"{SearchTools.LINK_PREFIX}{result[SearchTools.LINK_KEY]}",
                    f"{SearchTools.SNIPPET_PREFIX}{result[SearchTools.SNIPPET_KEY]}",
                    SearchTools.SEPARATOR
                ]))
            except KeyError:
                continue
        return '\n'.join(string)