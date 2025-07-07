from mcp.server.fastmcp import FastMCP
from typing import List
import json
import arxiv
import os

# Initialize the FastMCP server
mcp = FastMCP("Test")

PAPER_DIR = "papers"

@mcp.tool()
def search_paper(topic:str, max_results:int=5) -> List[str]:

    # Use arxiv to find the papers
    client = arxiv.Client()

    # Search the most relevant articles matching the queried topic
    search = client.search(
        query=topic, 
        max_results=max_results,
        sort_by= arxiv.SortCriterion.Relevance
        )
    
    papers = client.results(search)

    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as f:
            papers_info = json.load(f)
    except:
        papers_info = {}

    # Process each paper and add to papers_info
    paper_ids =[]
    for paper in papers:
        paper_ids.append(paper.get_short_id)
        paper_info={
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info

    # Save papers info to file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)

    print(f"Results are saved in: {file_path}")

    return paper_ids


@mcp.tool()
def extract_info(paper_id:str) -> str:
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id],indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path} : {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}"

  
if __name__ == "__main__":
    mcp.run(transport="stdio")
                    