# from crewai import WebsiteSearchTool
import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import DuckDuckGoSearchRun

def load_api_key():
    load_dotenv()
    return os.getenv('OPENAI_API_KEY')

load_dotenv()
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')

#web_tool = WebsiteSearchTool(website='https://my .com/v2/webhome/searchhotel')
tavily_tool = TavilySearchResults(k=5)
search_tool = DuckDuckGoSearchRun()