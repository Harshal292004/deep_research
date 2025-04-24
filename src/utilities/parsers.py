import re
from typing import List
from pydantic import BaseModel, Field
from typing import Union
from utilities.states import ArxivDoc,ArxivSearchOutput
def parse_arxiv_text(raw_text: str) -> ArxivSearchOutput:
    # Regex to split papers by "Published: ..."
    if raw_text == 'No good Arxiv Result was found':
        return ArxivSearchOutput(results='No good Arxiv Result was found')
    entries = re.split(r"\n(?=Published:)", raw_text.strip())
    results = []

    for entry in entries:
        published_match = re.search(r"Published:\s*(.*)", entry)
        title_match = re.search(r"Title:\s*(.*)", entry)
        authors_match = re.search(r"Authors:\s*(.*)", entry)
        summary_match = re.search(r"Summary:\s*((?:.|\n)*?)$", entry)

        if published_match and title_match and authors_match and summary_match:
            results.append(ArxivDoc(
                published=published_match.group(1).strip(),
                title=title_match.group(1).strip(),
                authors=[author.strip() for author in authors_match.group(1).split(",")],
                summary=summary_match.group(1).strip()
            ))
    
    return ArxivSearchOutput(results=results)
