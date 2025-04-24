# import requests
# from utilities.states import LocationOutput
# from pydantic import BaseModel, Field
# from typing import List, Literal, Union
# from utilities.states import (
#     DuckDuckGoOutput,
#     LocationOutput,
#     SereprSearchOutput,
#     OrganicItem,
# )

# def get_location()->LocationOutput:
#     response = requests.get('https://ipinfo.io/json')
#     result = response.json()
#     country= str(result["country"])
#     location_reuslt=LocationOutput(country=country.lower())
#     return location_reuslt

# loc = get_location()
# print(loc)

# data = {
#     "organic": [
#         {
#             "title": "Apple",
#             "link": "https://www.apple.com/",
#             "snippet": "Discover the innovative world of Apple and shop everything iPhone, iPad, Apple Watch, Mac, and Apple TV, plus explore accessories, entertainment, ...",
#             "sitelinks": [
#                 {"title": "Support", "link": "https://support.apple.com/"},
#                 {"title": "iPhone", "link": "https://www.apple.com/iphone/"},
#                 {
#                     "title": "Apple makes business better.",
#                     "link": "https://www.apple.com/business/",
#                 },
#                 {"title": "Mac", "link": "https://www.apple.com/mac/"},
#             ],
#             "position": 1,
#         },
#         {
#             "title": "Apple Inc. - Wikipedia",
#             "link": "https://en.wikipedia.org/wiki/Apple_Inc.",
#             "snippet": "Apple Inc. is an American multinational technology company specializing in consumer electronics, software and online services headquartered in Cupertino, ...",
#             "attributes": {
#                 "Products": "AirPods; Apple Watch; iPad; iPhone; Mac",
#                 "Founders": "Steve Jobs; Steve Wozniak; Ronald Wayne",
#                 "Founded": "April 1, 1976; 46 years ago in Los Altos, California, U.S",
#                 "Industry": "Consumer electronics; Software services; Online services",
#             },
#             "sitelinks": [
#                 {
#                     "title": "History",
#                     "link": "https://en.wikipedia.org/wiki/History_of_Apple_Inc.",
#                 },
#                 {
#                     "title": "Timeline of Apple Inc. products",
#                     "link": "https://en.wikipedia.org/wiki/Timeline_of_Apple_Inc._products",
#                 },
#                 {
#                     "title": "List of software by Apple Inc.",
#                     "link": "https://en.wikipedia.org/wiki/List_of_software_by_Apple_Inc.",
#                 },
#                 {
#                     "title": "Apple Store",
#                     "link": "https://en.wikipedia.org/wiki/Apple_Store",
#                 },
#             ],
#             "position": 2,
#         },
#         {
#             "title": "Apple Inc. | History, Products, Headquarters, & Facts | Britannica",
#             "link": "https://www.britannica.com/topic/Apple-Inc",
#             "snippet": "Apple Inc., formerly Apple Computer, Inc., American manufacturer of personal computers, smartphones, tablet computers, computer peripherals, ...",
#             "date": "Aug 31, 2022",
#             "attributes": {
#                 "Related People": "Steve Jobs Steve Wozniak Jony Ive Tim Cook Angela Ahrendts",
#                 "Date": "1976 - present",
#                 "Areas Of Involvement": "peripheral device",
#             },
#             "position": 3,
#         },
#         {
#             "title": "AAPL: Apple Inc Stock Price Quote - NASDAQ GS - Bloomberg.com",
#             "link": "https://www.bloomberg.com/quote/AAPL:US",
#             "snippet": "Stock analysis for Apple Inc (AAPL:NASDAQ GS) including stock price, stock chart, company news, key statistics, fundamentals and company profile.",
#             "position": 4,
#         },
#         {
#             "title": "Apple Inc. (AAPL) Company Profile & Facts - Yahoo Finance",
#             "link": "https://finance.yahoo.com/quote/AAPL/profile/",
#             "snippet": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related ...",
#             "position": 5,
#         },
#         {
#             "title": "AAPL | Apple Inc. Stock Price & News - WSJ",
#             "link": "https://www.wsj.com/market-data/quotes/AAPL",
#             "snippet": "Apple, Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other varieties of ...",
#             "position": 6,
#         },
#         {
#             "title": "Apple Inc Company Profile - Apple Inc Overview - GlobalData",
#             "link": "https://www.globaldata.com/company-profile/apple-inc/",
#             "snippet": "Apple Inc (Apple) designs, manufactures, and markets smartphones, tablets, personal computers (PCs), portable and wearable devices. The company also offers ...",
#             "position": 7,
#         },
#         {
#             "title": "Apple Inc (AAPL) Stock Price & News - Google Finance",
#             "link": "https://www.google.com/finance/quote/AAPL:NASDAQ?hl=en",
#             "snippet": "Get the latest Apple Inc (AAPL) real-time quote, historical performance, charts, and other financial information to help you make more informed trading and ...",
#             "position": 8,
#         },
#     ]
# }
# result = data["organic"]
# serper_output = []
# for item in result:
#     organic_item = OrganicItem(
#         title=item["title"], link=item["link"], snippet=item["snippet"]
#     )
#     serper_output.append(organic_item)


# serper_output_list = SereprSearchOutput(organic=serper_output)

# print(serper_output_list)

# from github import Github

# class GitHubInspector:
#     def __init__(self,token ):
#         self.g = Github(token)

#     def get_user_by_name(self, username):
#         user = self.g.get_user(username)
#         return {
#             "login": user.login,
#             "name": user.name,
#             "public_repos": user.public_repos,
#             "followers": user.followers,
#             "bio": user.bio,
#             "location": user.location,
#         }

#     def get_repo_by_name(self, full_name):
#         repo = self.g.get_repo(full_name)
#         return {
#             "name": repo.name,
#             "full_name": repo.full_name,
#             "description": repo.description,
#             "stars": repo.stargazers_count,
#             "forks": repo.forks_count,
#             "language": repo.language,
#             "topics": repo.get_topics()
#         }

#     def get_org_by_name(self, org_name):
#         org = self.g.get_organization(org_name)
#         return {
#             "login": org.login,
#             "name": org.name,
#             "description": org.description,
#             "public_repos": org.public_repos,
#             "members": [member.login for member in org.get_members()]
#         }
#     def search_repos_by_language(self, language, limit=10):
#         result = self.g.search_repositories(query=f"language:{language}")
#         return [{
#             "name": repo.name,
#             "full_name": repo.full_name,
#             "stars": repo.stargazers_count,
#             "url": repo.html_url
#         } for repo in result[:limit]]



# inspector = GitHubInspector("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")

# print(inspector.get_user_by_name("torvalds"))
# print("\n\n\n\n "+40*"="+ "\n\n\n\n")
# print(inspector.get_repo_by_name("torvalds/linux"))
# print("\n\n\n\n "+40*"="+ "\n\n\n\n")
# print(inspector.get_org_by_name("github"))
# print("\n\n\n\n "+40*"="+ "\n\n\n\n")
# print(inspector.get_repo_topics("torvalds/linux"))
# print("\n\n\n\n "+40*"="+ "\n\n\n\n")
# print(inspector.get_repo_star_count("torvalds/linux"))
# print("\n\n\n\n "+40*"="+ "\n\n\n\n")
# print(inspector.search_repos_by_language("TypeScript"))

from langchain_community.utilities.arxiv import ArxivAPIWrapper

def arxiv_search():
    arxiv = ArxivAPIWrapper(
        top_k_results = 3,
        ARXIV_MAX_QUERY_LENGTH = 300,
        load_max_docs = 3,
        load_all_available_meta = False,
        doc_content_chars_max = 40000
    )
    output= arxiv.run("tree of thought llm")
    print(f"type of the shit:{type(output)} \n\n\n")
    print(arxiv.run("tree of thought llm"))
    
arxiv_search()