import json
import os

import requests
from langchain.tools import tool
from tavily import TavilyClient


class SearchTools():

    @tool("Hotel Horison Search")
    def search_horison(query):
        """
        Useful to search the Horison Hotel in a specific city.
        If the Horison Hotel is not available, it returns relevant results from other sources.
        """
        # Step 1. Instantiating your TavilyClient
        tavily_client = TavilyClient(api_key="TAVILY_API_KEY")
        
        # Step 2. Defining the list of URLs to extract content from
        urls = [
            "https://myhorison.com/"
            "https://www.traveloka.com/"
        ]
        
        # Step 3. Executing the extract request
        response = tavily_client.extract(urls=urls)

        horison_found = any("Horison" in result['raw_content'] for result in response["results"])

        if not horison_found:
            urls = [
                "https://www.google.com/",
                "https://www.traveloka.com/"
            ]
            response = tavily_client.extract(urls=urls)

        # Step 4. Printing the extracted raw content
        extracted_content = []
        for result in response["results"]:
            extracted_content.append(f"URL: {result['url']}")
            extracted_content.append(f"Raw Content: {result['raw_content']}\n")
        
        return '\n'.join(extracted_content)