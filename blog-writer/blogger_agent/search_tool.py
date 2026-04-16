from langchain_community.tools import DuckDuckGoSearchRun

def search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Compatible with OpenAI models in ADK.
    """
    search_tool = DuckDuckGoSearchRun()
    return search_tool.run(query)