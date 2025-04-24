import requests
from utilities.states import LocationOutput
from pydantic import BaseModel, Field
from typing import List, Literal, Union
from utilities.states import (
    DuckDuckGoOutput,
    LocationOutput,
    SereprSearchOutput,
    OrganicItem,
)

# def get_location()->LocationOutput:
#     response = requests.get('https://ipinfo.io/json')
#     result = response.json()
#     country= str(result["country"])
#     location_reuslt=LocationOutput(country=country.lower())
#     return location_reuslt

# loc = get_location()
# print(loc)

data = {
    "organic": [
        {
            "title": "Apple",
            "link": "https://www.apple.com/",
            "snippet": "Discover the innovative world of Apple and shop everything iPhone, iPad, Apple Watch, Mac, and Apple TV, plus explore accessories, entertainment, ...",
            "sitelinks": [
                {"title": "Support", "link": "https://support.apple.com/"},
                {"title": "iPhone", "link": "https://www.apple.com/iphone/"},
                {
                    "title": "Apple makes business better.",
                    "link": "https://www.apple.com/business/",
                },
                {"title": "Mac", "link": "https://www.apple.com/mac/"},
            ],
            "position": 1,
        },
        {
            "title": "Apple Inc. - Wikipedia",
            "link": "https://en.wikipedia.org/wiki/Apple_Inc.",
            "snippet": "Apple Inc. is an American multinational technology company specializing in consumer electronics, software and online services headquartered in Cupertino, ...",
            "attributes": {
                "Products": "AirPods; Apple Watch; iPad; iPhone; Mac",
                "Founders": "Steve Jobs; Steve Wozniak; Ronald Wayne",
                "Founded": "April 1, 1976; 46 years ago in Los Altos, California, U.S",
                "Industry": "Consumer electronics; Software services; Online services",
            },
            "sitelinks": [
                {
                    "title": "History",
                    "link": "https://en.wikipedia.org/wiki/History_of_Apple_Inc.",
                },
                {
                    "title": "Timeline of Apple Inc. products",
                    "link": "https://en.wikipedia.org/wiki/Timeline_of_Apple_Inc._products",
                },
                {
                    "title": "List of software by Apple Inc.",
                    "link": "https://en.wikipedia.org/wiki/List_of_software_by_Apple_Inc.",
                },
                {
                    "title": "Apple Store",
                    "link": "https://en.wikipedia.org/wiki/Apple_Store",
                },
            ],
            "position": 2,
        },
        {
            "title": "Apple Inc. | History, Products, Headquarters, & Facts | Britannica",
            "link": "https://www.britannica.com/topic/Apple-Inc",
            "snippet": "Apple Inc., formerly Apple Computer, Inc., American manufacturer of personal computers, smartphones, tablet computers, computer peripherals, ...",
            "date": "Aug 31, 2022",
            "attributes": {
                "Related People": "Steve Jobs Steve Wozniak Jony Ive Tim Cook Angela Ahrendts",
                "Date": "1976 - present",
                "Areas Of Involvement": "peripheral device",
            },
            "position": 3,
        },
        {
            "title": "AAPL: Apple Inc Stock Price Quote - NASDAQ GS - Bloomberg.com",
            "link": "https://www.bloomberg.com/quote/AAPL:US",
            "snippet": "Stock analysis for Apple Inc (AAPL:NASDAQ GS) including stock price, stock chart, company news, key statistics, fundamentals and company profile.",
            "position": 4,
        },
        {
            "title": "Apple Inc. (AAPL) Company Profile & Facts - Yahoo Finance",
            "link": "https://finance.yahoo.com/quote/AAPL/profile/",
            "snippet": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related ...",
            "position": 5,
        },
        {
            "title": "AAPL | Apple Inc. Stock Price & News - WSJ",
            "link": "https://www.wsj.com/market-data/quotes/AAPL",
            "snippet": "Apple, Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other varieties of ...",
            "position": 6,
        },
        {
            "title": "Apple Inc Company Profile - Apple Inc Overview - GlobalData",
            "link": "https://www.globaldata.com/company-profile/apple-inc/",
            "snippet": "Apple Inc (Apple) designs, manufactures, and markets smartphones, tablets, personal computers (PCs), portable and wearable devices. The company also offers ...",
            "position": 7,
        },
        {
            "title": "Apple Inc (AAPL) Stock Price & News - Google Finance",
            "link": "https://www.google.com/finance/quote/AAPL:NASDAQ?hl=en",
            "snippet": "Get the latest Apple Inc (AAPL) real-time quote, historical performance, charts, and other financial information to help you make more informed trading and ...",
            "position": 8,
        },
    ]
}
result = data["organic"]
serper_output = []
for item in result:
    organic_item = OrganicItem(
        title=item["title"], link=item["link"], snippet=item["snippet"]
    )
    serper_output.append(organic_item)


serper_output_list = SereprSearchOutput(organic=serper_output)

print(serper_output_list)
