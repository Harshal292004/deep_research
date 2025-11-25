"""Tool output formatter"""
from backend.src.models.report import Reference, Section
from backend.src.models.tools import (
    ToolOutputState
)
from backend.src.helpers.logger import log

def roll_out_output(state: ToolOutputState, refrence: Reference, section: Section):
    """Format tool output into string and collect references"""
    try:
        rolled_out_str = ""
        refrence.section_name = section.name
        refrence.section_id = section.section_id

        if state.duckduckgo_output:
            rolled_out_str += "DUCK DUCK GO SEARCH:\n\n\n"
            for duck in state.duckduckgo_output:
                duck_string = f"{duck.title} {duck.snippet}\n\n"
                duck_string = duck_string[:1000]
                rolled_out_str += f"{duck_string}\n\n"
                refrence.source_url.append(duck.link)

        if state.exa_output:
            rolled_out_str += "EXA SEARCH:\n\n\n"
            for exa in state.exa_output:
                highlight_string = "".join(exa.highlights)
                highlight_string = highlight_string[:1000]
                rolled_out_str += f"{highlight_string} \n\n"
                refrence.source_url.append(exa.url)

        if state.serper_output:
            rolled_out_str += "SERPER SEARCH:\n\n\n"
            for organic in state.serper_output.organic_results:
                organic_string = f"{organic.title} {organic.snippet} \n\n"
                organic_string = organic_string[:2000]
                rolled_out_str += organic_string
                refrence.source_url.append(organic.link)

        if state.github_user_output:
            rolled_out_str += "GITHUB USER:\n\n\n"
            gh = state.github_user_output
            rolled_out_str += f"Github username: {gh.login} User's full name: {gh.name} Number of public repos: {gh.public_repos} Number of followers: {gh.followers} Bio of the user: {gh.bio} Location of the user: {gh.location}\n\n"
            refrence.source_url.append(f"https://github.com/{gh.login}")

        if state.github_repo_output:
            rolled_out_str += "GITHUB REPO:\n\n"
            gh = state.github_repo_output
            topic_str = "\n".join(gh.topics)
            rolled_out_str += f"Github Repo name: {gh.name} Repo's full name: {gh.full_name} Description of repo: {gh.description} Number of stars: {gh.stars} Number of forks: {gh.forks} Language used: {gh.language} Topics:\n{topic_str}\n\n"
            refrence.source_url.append(f"https://github.com/{gh.full_name}")

        if state.github_org_output:
            rolled_out_str += "GITHUB ORG:\n\n"
            gh = state.github_org_output
            member_list = "".join(gh.members)
            rolled_out_str += f"Github Org login: {gh.login} Org's full name: {gh.name} Org's description: {gh.description} Number of public_repo: {gh.public_repos} Member of repo: {member_list}\n\n"
            refrence.source_url.append(f"https://github.com/{gh.login}")

        if state.github_language_output:
            rolled_out_str += "GITHUB REPO Based on language:\n\n"
            for gh in state.github_language_output.results:
                rolled_out_str += f"Github repo's name: {gh.name} Repo's full name: {gh.full_name} Number of stars: {gh.stars} URL of the repo: {gh.url}\n\n"
                refrence.source_url.append(gh.url)

        if state.arxiv_output:
            rolled_out_str += "ARXIV Output:\n\n"
            if isinstance(state.arxiv_output.results, list):
                for axv in state.arxiv_output.results:
                    author_str = "  ".join(axv.authors[:4])
                    arxiv_string = f"Paper Title: {axv.title} Authors: {author_str} Summary: {axv.summary[:200]} Published: {axv.published}\n\n"
                    rolled_out_str += arxiv_string
                    # Note: ArxivDoc doesn't have url, would need to add if needed

        if state.tavily_output:
            rolled_out_str += "TAVILY Output:\n\n"
            for tav in state.tavily_output.results:
                tavily_string = f"Title: {tav.title} Content: {tav.content} \n\n"
                tavily_string = tavily_string[:500]
                rolled_out_str += tavily_string
                refrence.source_url.append(tav.url)

        return rolled_out_str, refrence
    except Exception as e:
        log.error(f"Error occurred in roll_out_output: {e}")
        return None, None

