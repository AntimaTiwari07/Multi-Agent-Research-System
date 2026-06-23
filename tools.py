from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()
import requests #web scrapping
from bs4 import BeautifulSoup #web scrapping
from tavily import TavilyClient
import os
from rich import print

# fetch web content from a given tavily tool
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """ Search the web for recent and reliable information of a topic.Returns titles,URLs and snippets."""
    results = tavily.search(query=query,max_results=5)
    out = []
    for r in results['results']:
      out.append(
         f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
      )
    return "\n--------\n".join(out)

@tool
def scrape_url(url:str)->str:
    """Scrape the content of a given URL and return the deeper details."""
    try:
        response = requests.get(url,timeout=8,headers={'User-Agent': 'Mozilla/5.0'})  # Set a user-agent to avoid blocking
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from the page
        for tag in soup(['script', 'style',"nav","header","footer"]):
            tag.decompose()  # Remove script and style elements
            return soup.get_text(separator=" ", strip=True)[:3000]
    except requests.exceptions.RequestException as e:
        print(f"[red]Error fetching URL {url}: {e}[/red]")
        return ""
