# section writer first but with the same grah but with differnet agents
from nodes import (
  router_node,
  header_writer_node,
  section_writer_node,
  footer_writer_node,
  verify_report_node,
  query_generation_node,
  tool_output_node,
  detailed_footer_writer_node,
  detailed_header_writer_node,
  detailed_section_writer_node,
  report_formatter_node
)
from typing import Optional
from edges import verify_conditional_edge
from observability.langfuse_setup import langfuse_handler
from utilities.states.report_state import ReportState,WriterState
from utilities.states.research_state import ResearchState
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from utilities.helpers.logger import log
section_builder = StateGraph(ReportState)
# register nodes
section_builder.add_node("router_node", router_node)
section_builder.add_node("header_writer_node", header_writer_node)
section_builder.add_node("section_writer_node", section_writer_node)
section_builder.add_node("footer_writer_node", footer_writer_node)
section_builder.add_node("verify_report_node", verify_report_node)
# edges
section_builder.add_edge(START, "router_node")
section_builder.add_edge("router_node", "header_writer_node")
section_builder.add_edge("header_writer_node", "section_writer_node")
section_builder.add_edge("section_writer_node", "footer_writer_node")
section_builder.add_edge("footer_writer_node", "verify_report_node")
section_builder.add_conditional_edges("verify_report_node", verify_conditional_edge)

memory = MemorySaver()
section_graph = section_builder.compile(checkpointer=memory)


# Research Agent

research_builder= StateGraph(ResearchState)

research_builder.add_node("query_generation_node",query_generation_node)
research_builder.add_node("tool_output_node",tool_output_node)

research_builder.add_edge(START,"query_generation_node")
research_builder.add_edge("query_generation_node","tool_output_node")
research_builder.add_edge("tool_output_node",END)

research_graph= research_builder.compile(checkpointer=memory)

# Writer Agent

writer_builder= StateGraph(WriterState)

writer_builder.add_node("detailed_section_writer_node",detailed_section_writer_node)
writer_builder.add_node("detailed_header_writer_node",detailed_header_writer_node)
writer_builder.add_node("detailed_footer_writer_node",detailed_footer_writer_node)
writer_builder.add_node("report_formatter_node",report_formatter_node)

writer_builder.add_edge(START,"detailed_section_writer_node")
writer_builder.add_edge("detailed_section_writer_node","detailed_header_writer_node")
writer_builder.add_edge("detailed_header_writer_node","detailed_footer_writer_node")
writer_builder.add_edge("detailed_footer_writer_node","report_formatter_node")
writer_builder.add_edge("report_formatter_node",END)


writer_graph= writer_builder.compile(checkpointer=memory)

async def main():
    report_state:Optional[ReportState] = None
    research_state:Optional[ResearchState] = None
    writer_state:Optional[WriterState] = None
    
    # async for state in section_graph.astream(
    #     {
    #         "query": "What is the current status of the american tariffs?",
    #         "user_feedback": " ",
    #     },
    #     stream_mode=["values"],
    #     config={
    #         "callbacks": [langfuse_handler],
    #         "configurable": {"thread_id": "abc123"},
    #     },
    # ):
    #     report_state = state 
        
    # report_state= ReportState(**report_state[1])
    
    # async for state in research_graph.astream(
    #     {
    #         "query":report_state.query,
    #         "type_query":report_state.type_of_query,
    #         "sections":report_state.sections.sections
    #     },
    #     stream_mode=["values"],
    #     config={
    #         "callbacks":[langfuse_handler],
    #         "configurable":{"thread_id":"abc123"}
    #     }
    # ):
    #     research_state= state
    
    # research_state=ResearchState(**research_state[1])
    
    # log.debug(f"The research state queries are: {research_state.queries}")
    # log.debug(f"\n\n\n\nThe research state outputs are: {research_state.outputs}")

    
    
    # async for state in writer_graph.astream(
    #     {
    #         "query":report_state.query,
    #         "type_query":report_state.type_of_query,
    #         "sections":report_state.sections,
    #         "output_list": research_state.outputs,
    #         "header":report_state.header,
    #         "footer":report_state.footer,
    #     },
    #     config={
    #         "callbacks":[langfuse_handler],
    #         "configurable":{"thread_id":"abc123"}
    #     }
    # ):
    #     writer_state= state
    #     print(writer_state)
    # print("Final Writer State:",writer_state)
    
    
    async for state in writer_graph.astream(
            {
                "query": "What is the current status of the american tariffs?",
                "type_of_query": "factual_query",
                "outputs": [
                    {
                        "section_id": "b744e004-93d0-4c82-80fc-e947e618ca14",
                        "output_state": {
                            "duckduckgo_output": [
                                {
                                    "title": "New Tariff Requirements 2025 Factsheet - U.S. Customs and Border Protection",
                                    "link": "https://www.cbp.gov/document/fact-sheets/new-tariff-requirements-2025-factsheet",
                                    "snippet": "The New Tariff Requirements 2025 Factsheet will provide information on Executive Orders and Proclamations that have imposed new tariffs on goods imported into the United States pursuant to the International Emergency Economic Powers Act (IEEPA) and Section 232 of the Trade Expansion Act of 1962."
                                },
                                {
                                    "title": "Official CBP Statement On Tariffs",
                                    "link": "https://www.cbp.gov/newsroom/announcements/official-cbp-statement-tariffs",
                                    "snippet": "On March 4, 2025 and March 7, 2025, U.S. Customs and Border Protection (CBP) implemented five Presidential Executive Orders implementing tariff updates for imports from China, Hong Kong, Canada, and Mexico. Pursuant to these Executive Orders, CBP is collecting the following additional tariffs on imports from Mexico, Canada, and China under the International Emergency Economic Powers Act:"
                                },
                                {
                                    "title": "U.S. Tariff Rates by Country - Trump Reciprocal Tariffs, April 2025",
                                    "link": "https://passportglobal.com/us-tariff-rates-by-country-2025/",
                                    "snippet": "View the latest U.S. tariff rates by country under Trump's April 2025 reciprocal tariff policy. See which countries face higher import duties and how rates compare. ... Instead, effective April 10, 2025, a flat 10% tariff applies to imports from all countries. China and Hong Kong are the exception: imports from these countries are subject to ..."
                                },
                                {
                                    "title": "Regulating Imports with a Reciprocal Tariff to Rectify Trade Practices ...",
                                    "link": "https://www.whitehouse.gov/presidential-actions/2025/04/regulating-imports-with-a-reciprocal-tariff-to-rectify-trade-practices-that-contribute-to-large-and-persistent-annual-united-states-goods-trade-deficits/",
                                    "snippet": "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq ..."
                                }
                            ],
                            "exa_output": [
                                {
                                    "highlights": [
                                        "President Donald Trump has launched tariff wars with almost all of America’s trading partners Mark Schiefelbein President Donald Trump speaks during an event to announce new tariffs in the Rose Garden at the White House, Wednesday, April 2, 2025, in Washington. (AP Photo/Mark Schiefelbein) Galleries"
                                    ],
                                    "url": "https://www.usnews.com/news/business/articles/2025-04-08/trumps-latest-round-of-tariffs-are-poised-to-go-into-effect-heres-what-we-know"
                                },
                                {
                                    "highlights": [
                                        "Nearly $1.5 trillion of public and private funds have been channeled into these industries in the past few years. While Biden criticized Trump’s tariffs during the 2020 campaign, he kept almost all of them in place once in office. On Tuesday, Ambassador Katherine Tai, his chief trade negotiator, confirmed that they would remain in effect, despite U.S. industry hopes that they would be narrowed. “We’re not going to let China flood our market,” the president said. The White House also blasted the trade deal with China that Trump signed in 2020, saying it failed to increase American exports or manufacturing jobs."
                                    ],
                                    "url": "https://www.washingtonpost.com/business/2024/05/14/biden-china-tariff-ev-solar/"
                                },
                                {
                                    "highlights": [
                                        "According to WTO data, China exported $30.9 billion medical goods to the United States in 2022, accounting for about one fifth of China's overall exports of medical goods. The expected tariffs are part of the Biden administration's broader strategy to protect the U.S. against supply shortages seen during the pandemic that left hospitals scrambling to find critical equipment, the sources said. In December, the United States Trade Representative announced a further extension of China-related \"Section 301\" tariff exclusions until May 31. The American Medical Manufacturers Association has called for these exclusions to be revoked, arguing they are no longer needed to deal with a COVID-19 emergency. The association says American manufacturers need the chance to compete with imports on a more level playing field."
                                    ],
                                    "url": "https://www.reuters.com/world/how-hard-will-new-biden-tariffs-hit-china-2024-05-13/"
                                },
                                {
                                    "highlights": [
                                        " - [On-Air Status](https://ktvz.com/about-us/on-air-status/)  - [Receiving KTVZ](https://ktvz.com/about-us/receiving-ktvz/)  - [TV Listings](https://ktvz.com/about-us/tv-listings/) The fresh duties, [announced by](https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/202502/t20250204_3955222.htm) China’s Ministry of Finance, levy a 15% tax on certain types of coal and liquefied natural gas and a 10% tariff on crude oil, agricultural machinery, large-displacement cars and pickup trucks. The measures take effect on February 10."
                                    ],
                                    "url": "https://ktvz.com/money/cnn-business-consumer/2025/02/03/china-hits-back-as-trumps-tariffs-go-into-effect/"
                                },
                                {
                                    "highlights": [
                                        "China denounced the new tariffs on its exports, with Beijing saying it would challenge them at the World Trade Organization and take unspecified “countermeasures.” The U.S. had a $279 billion trade deficit with China in 2023, the largest figure for any of its trading partners. - [! [UK's Starmer seeks strong trade relations with the US in the wake of Trump's tariffs ](https://www.voanews.com/a/trump-to-speak-with-canadian-mexican-leaders-after-imposing-new-tariffs/7960635.html)](https://www.voanews.com/a/uk-s-starmer-germany-s-scholz-meet-as-eu-reset-looms/7960082.html) - [! [Facing tariff threats, India lowers import duties to signal it is not protectionist ](https://www.voanews.com/a/trump-to-speak-with-canadian-mexican-leaders-after-imposing-new-tariffs/7960635.html)](https://www.voanews.com/a/facing-tariff-threats-india-lowers-import-duties-to-signal-it-is-not-protectionist-/7960808.html)"
                                    ],
                                    "url": "https://www.voanews.com/a/trump-to-speak-with-canadian-mexican-leaders-after-imposing-new-tariffs/7960635.html"
                                }
                            ],
                            "tavily_output": {
                                "results": [
                                    {
                                        "title": "Trump tariffs live updates: China says 'door is open' to trade talks ...",
                                        "url": "https://finance.yahoo.com/news/live/trump-tariffs-live-updates-china-says-door-is-open-to-trade-talks-with-the-us-191201877.html",
                                        "content": "Trump tariffs live updates: China says 'door is open' to trade talks with the US Trump tariffs live updates: China says 'door is open' to trade talks with the US President Donald Trump said he is willing to lower tariffs on China at some point because the levies now are so high that the world’s two largest economies have essentially stopped doing business with each other. Manufacturing activity across most of Asia contracted in April, as companies struggled with weaker demand and paused new orders in response to President Trump’s baseline 10% tariff on goods imported from China."
                                    },
                                    {
                                        "title": "Tariff Tracker: Where Do President Trump's Trade Proposals Stand?",
                                        "url": "https://www.investopedia.com/tariff-tracker-where-do-president-trump-trade-proposals-stand-11702803",
                                        "content": "President Donald Trump has imposed sweeping tariffs on U.S. trading partners and promised that more will be implemented. |  Mexico | Enacted March 4 | 25% | Trump Delays Mexico, Canada Tariffs | Executive Order | | Canada | Enacted March 4 | 25% | Trump Delays Mexico, Canada Tariffs | Executive Order | Trump paused these tariffs for 90 days in order to negotiate trade deals with more than 75 countries, he said on April 9, just hours after the tariffs were implemented. On April 29, Trump signed an executive order that exempted imported vehicles from other tariffs, such as the steel tariff or the 10% tariff on goods from most countries."
                                    },
                                    {
                                        "title": "Tracking Every Trump Tariff and Its Economic Effect - Bloomberg.com",
                                        "url": "https://www.bloomberg.com/graphics/trump-tariffs-tracker/",
                                        "content": "Trump Tariffs: Track Targeted Goods and Economic Impact Worldwide Bloomberg Bloomberg Tracking Every Trump Tariff and Its Economic Effect US President Donald Trump announced a 90-day pause on higher reciprocal tariffs that hit dozens of trade partners, while raising duties on China to 125%. Read more: Trump to Impose 10% Global Tariffs on US Imports, WSJ Says → Read more: Trump Escalates Global Trade War, Sparking Tit-for-Tat Tariffs → Read more: Trump’s Threat of ‘Secondary Tariffs’ Invents New Trade Tool → Trump Tariffs Target Some of Americans’ Favorite Imports → Steel and aluminum are per published tariff product lists, and effective 2024 tariffs are used to calculate the impact of removing exemptions; Autos are from pre-publication tariff product list."
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "section_id": "d2e33319-9132-44c6-a44c-a138dca9573b",
                        "output_state": {
                            "duckduckgo_output": [
                                {
                                    "title": "New Tariff Requirements 2025 Factsheet - U.S. Customs and Border Protection",
                                    "link": "https://www.cbp.gov/document/fact-sheets/new-tariff-requirements-2025-factsheet",
                                    "snippet": "The New Tariff Requirements 2025 Factsheet will provide information on Executive Orders and Proclamations that have imposed new tariffs on goods imported into the United States pursuant to the International Emergency Economic Powers Act (IEEPA) and Section 232 of the Trade Expansion Act of 1962."
                                },
                                {
                                    "title": "See what tariffs are currently in place, who's impacted by trade war",
                                    "link": "https://www.usatoday.com/story/graphics/2025/04/10/current-trump-tariffs-map/83026822007/",
                                    "snippet": "The U.S. economy has been riding a financial roller coaster driven by President Donald Trump's trade war and his April 2 announcement of tariffs on imports to all U.S. trading partners. Trump ..."
                                },
                                {
                                    "title": "Regulating Imports with a Reciprocal Tariff to Rectify Trade Practices ...",
                                    "link": "https://www.whitehouse.gov/presidential-actions/2025/04/regulating-imports-with-a-reciprocal-tariff-to-rectify-trade-practices-that-contribute-to-large-and-persistent-annual-united-states-goods-trade-deficits/",
                                    "snippet": "By the authority vested in me as President by the Constitution and the laws of the United States of America, including the International Emergency Economic Powers Act (50 U.S.C. 1701 et seq ..."
                                },
                                {
                                    "title": "2025 U.S. Tariffs Update - New Trade Policies & Ecommerce Impact ...",
                                    "link": "https://zonos.com/docs/guides/2025-us-tariff-changes",
                                    "snippet": "The reciprocal tariffs aim to establish fair trade by aligning U.S. tariffs with those levied by other countries on American products. This policy is expected to introduce new tariff structures affecting multiple trade partners, with a pending effective date of April 2, 2025. February 10, 2025"
                                }
                            ],
                            "exa_output": [
                                {
                                    "highlights": [
                                        "President Donald Trump has launched tariff wars with almost all of America’s trading partners Mark Schiefelbein President Donald Trump speaks during an event to announce new tariffs in the Rose Garden at the White House, Wednesday, April 2, 2025, in Washington. (AP Photo/Mark Schiefelbein) Galleries"
                                    ],
                                    "url": "https://www.usnews.com/news/business/articles/2025-04-08/trumps-latest-round-of-tariffs-are-poised-to-go-into-effect-heres-what-we-know"
                                },
                                {
                                    "highlights": [
                                        "KPMG International Limited is a private English company limited by guarantee and does not provide services to clients. No member firm has any authority to obligate or bind KPMG International or any other member firm vis-à-vis third parties, nor does KPMG International have any such authority to obligate or bind any member firm. The information contained herein is of a general nature and is not intended to address the circumstances of any particular individual or entity. Although we endeavor to provide accurate and timely information, there can be no guarantee that such information is accurate as of the date it is received or that it will continue to be accurate in the future. No one should act on such information without appropriate professional advice after a thorough examination of the particular situation."
                                    ],
                                    "url": "https://kpmg.com/us/en/taxnewsflash/news/2025/03/united-states-duty-free-de-minimis-treatment-canada-mexico.html"
                                },
                                {
                                    "highlights": [
                                        "[UK's Starmer seeks strong trade relations with the US in the wake of Trump's tariffs ](https://www.voanews.com/a/trump-to-speak-with-canadian-mexican-leaders-after-imposing-new-tariffs/7960635.html)](https://www.voanews.com/a/uk-s-starmer-germany-s-scholz-meet-as-eu-reset-looms/7960082.html) - [! [Facing tariff threats, India lowers import duties to signal it is not protectionist ](https://www.voanews.com/a/trump-to-speak-with-canadian-mexican-leaders-after-imposing-new-tariffs/7960635.html)](https://www.voanews.com/a/facing-tariff-threats-india-lowers-import-duties-to-signal-it-is-not-protectionist-/7960808.html) - [! - [!"
                                    ],
                                    "url": "https://www.voanews.com/a/trump-to-speak-with-canadian-mexican-leaders-after-imposing-new-tariffs/7960635.html"
                                }
                            ],
                            "tavily_output": {
                                "results": [
                                    {
                                        "title": "Tariff Tracker: Where Do President Trump's Trade Proposals Stand?",
                                        "url": "https://www.investopedia.com/tariff-tracker-where-do-president-trump-trade-proposals-stand-11702803",
                                        "content": "The 25% tariff will be imposed on goods imported into the U.S. from countries that buy Venezuelan oil. This could include China, the Dominican Republic, India, Malaysia, Russia, Singapore, Spain"
                                    },
                                    {
                                        "title": "Tracking Every Trump Tariff and Its Economic Effect - Bloomberg.com",
                                        "url": "https://www.bloomberg.com/graphics/trump-tariffs-tracker/",
                                        "content": "Keeping up with what goods are being targeted by US tariffs and what the economic impacts are. ... Tariff Impact on US. Affected Trade. $987.7B. Average Effective Tariff Rate +3%. GDP -0.4%."
                                    },
                                    {
                                        "title": "The impact of tariffs is coming. Which households will Trump's new plan ...",
                                        "url": "https://finance.yahoo.com/news/impact-tariffs-coming-households-trumps-191042296.html",
                                        "content": "Tariff impact: What grocery items may cost more due to Trump's tariffs? Seafood, coffee, olive oil, more Seafood, coffee, olive oil, more Why low-income households would pay more"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "section_id": "bb6b474e-3e90-43a6-a2ed-b7ce9f8c885d",
                        "output_state": {
                            "duckduckgo_output": [
                                {
                                    "title": "Tariffs: Estimating the Economic Impact of the 2025 Measures and ...",
                                    "link": "https://www.richmondfed.org/publications/research/economic_brief/2025/eb_25-12",
                                    "snippet": "A newer Economic Brief has been released that updates this analysis with the April 2 tariff announcement of a global tariff plan.. Tariffs are taxes imposed by a government on imported goods, typically calculated as a percentage of the import's value (known as an ad valorem tax). Governments use tariffs for various purposes, such as raising revenue, protecting domestic industries from foreign ..."
                                },
                                {
                                    "title": "The Economic Effects of President Trump's Tariffs",
                                    "link": "https://budgetmodel.wharton.upenn.edu/issues/2025/4/10/economic-effects-of-president-trumps-tariffs",
                                    "snippet": "Key Points. Revenue Impact: President Trump's tariff plan (as of April 8, 2025) is projected to raise significant revenue—over $5.2 trillion over 10 years on a conventional basis (with micro-elastic responses) and $4.5 trillion on a dynamic basis (with economic effects). This revenue could be used to reduce federal debt, thereby encouraging private investment."
                                },
                                {
                                    "title": "The economic impact of tariffs on business | McKinsey",
                                    "link": "https://www.mckinsey.com/capabilities/geopolitics/our-insights/tariffs-and-global-trade-the-economic-impact-on-business",
                                    "snippet": "Since the United States' announcement of reciprocal tariffs on April 2, 2025, financial markets around the world have seen heightened volatility, raising concerns about the impact on the global economy. The combined tariffs enacted by the US government since that date have rapidly raised the country's weighted-average tariff rate to its highest level in the past 100 years, from ..."
                                },
                                {
                                    "title": "US tariffs impact economy | Deloitte Insights",
                                    "link": "https://www2.deloitte.com/us/en/insights/economy/spotlight/united-states-tariffs-impact-economy.html",
                                    "snippet": "Tariffs have been dominating headlines as the new US administration drives sharp policy changes. In April, the United States announced a slew of reciprocal tariffs on almost all of its trading partners. 1 Goods from China will now attract a cumulative tariff hike of 125%. Most other countries and the European Union will face 10% tariffs for a period of 90 days to enable trade negotiations."
                                }
                            ],
                            "exa_output": [
                                {
                                    "highlights": [
                                        "tech sector compete with other less well-funded eforts  to meet the growing needs from increased population  sources, to fuel economic growth in certain countries and  concern to our clients. According to IBM’s Cost of "
                                    ],
                                    "url": "https://www.sec.gov/Archives/edgar/data/746838/000110465925027323/tm256765d2_ars.pdf"
                                },
                                {
                                    "highlights": [
                                        "and opportunistically. It also provides us with the flexibility to shift purchases between suppliers and categories. This enables us to obtain better terms with our suppliers, which we expect to help offset any rising costs of goods. Furthermore, we believe the “treasure hunt” nature of the off-price buying experience drives frequent"
                                    ],
                                    "url": "https://www.sec.gov/Archives/edgar/data/1579298/000119312525072378/d914810dars.pdf"
                                },
                                {
                                    "highlights": [
                                        "commodity prices, acreage planted, crop yields, and government policies, including global trade policies, and the amount and timing of  government payments. Sales also are influenced by general economic conditions, farmland prices, farmers’ debt levels and access to  financing, interest and exchange rates, agricultural trends, including the production of and demand for renewable fuels, labor  availability and costs, energy costs and related policies, tax policies, policies related to climate change, and other input costs "
                                    ],
                                    "url": "https://www.sec.gov/Archives/edgar/data/315189/000155837025000116/de-20241027xars.pdf"
                                },
                                {
                                    "highlights": [
                                        "for electric and hybrid vehicles and support growth and  improvements in the electric infrastructure. We are investing  to meet that demand by adding capacity at our electrical steel  facilities in Canada and Mexico, and we entered the European "
                                    ],
                                    "url": "https://www.sec.gov/Archives/edgar/data/1968487/000119312524202147/d807063dars.pdf"
                                },
                                {
                                    "highlights": [
                                        "sales force, while a network of independent sales representatives, and to a lesser extent independent distributors purchasing products for resale, are also utilized. The Company’s major requirements for basic raw materials include steel, cast iron, electronics, rare earth metals, aluminum and brass; and to a lesser extent, plastics and petroleum-based chemicals. The Company seeks to have"
                                    ],
                                    "url": "https://www.sec.gov/Archives/edgar/data/32604/000003260424000061/fy24annualreport-websitefi.pdf"
                                }
                            ],
                            "tavily_output": {
                                "results": [
                                    {
                                        "title": "The Surprising History Of Tariffs And Their Role In U.S. Economic Policy",
                                        "url": "https://www.forbes.com/sites/greatspeculations/2025/02/18/the-surprising-history-of-tariffs-and-their-role-in-us-economic-policy/",
                                        "content": "The Surprising History Of Tariffs And Their Role In U.S. Economic Policy The Surprising History Of Tariffs And Their Role In U.S. Economic Policy By imposing tariffs, the U.S. can pressure trading partners into more favorable deals and protect domestic industries from unfair competition. China has already retaliated, imposing its own tariffs on U.S. goods. In light of these developments, President Trump has floated an interesting idea: using tariff revenue to fund a U.S. sovereign wealth fund (SWF). Could the U.S. Wealth Fund Hold Bitcoin? Most SWFs are built from surpluses, but the U.S. runs a trade deficit, meaning we import more than we export. Trade policy changes can create volatility, but long-term opportunities exist in sectors resilient to tariffs."
                                    },
                                    {
                                        "title": "The Price-Inflation Paradox: How Tariffs Really Affect The Economy - Forbes",
                                        "url": "https://www.forbes.com/sites/billconerly/2024/11/21/the-price-inflation-paradox-how-tariffs-really-affect-the-economy/",
                                        "content": "The Price-Inflation Paradox: How Tariffs Really Affect The Economy Anticipation of incoming president Trump’s tariffs has caused confusion regarding high prices and high inflation. The effect of tariffs is to push prices up, but not to sustain higher inflation. The higher tariffs push prices up once, but the tariffs don’t change the inflation rate in later years. When tariffs push prices up, it will feel like inflation to consumers. The key difference is that for tariffs to push inflation to a higher sustained rate (shown on the chart as a steeper line), tariffs would have to increase year after year after year. A one-time shift in consumer prices does not cause a sustained increase in the inflation rate."
                                    },
                                    {
                                        "title": "Tariffs Are Hitting The U.S. Economy Where It Hurts - Investopedia",
                                        "url": "https://www.investopedia.com/tariffs-are-hitting-the-economy-where-it-hurts-11705264",
                                        "content": "In February, U.S. households cut back their spending on services while ramping up purchases of goods, which is a possible sign that people are rushing to buy things before tariffs hit, according to a report on spending and inflation from the Bureau of Economic Analysis on Friday. Consumer Anxiety Could Mean Slower Retail Sales Growth This Year Fed Officials Warn of the Challenge Trump Tariff 'Uncertainty' Poses Trump's Latest Round Of Tariffs Set to Make Cars More Expensive, Stoke Inflation Consumers Haven't Felt This Bad About the Economy Since 2022 OECD Cuts US, Global Economic Outlooks on 'Higher Trade Barriers' Canadian Summer Flight Bookings to US Down 70% From Last Year, Data Shows Inflation Ticked Down Faster Than Expected Ahead Of Tariff Turmoil Why the Dollar Is Having Its Worst Year Since 2008, and What It Means For You"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "section_id": "4ff8ad8f-43ef-49e1-bf8c-654a670ccc2b",
                        "output_state": {
                            "duckduckgo_output": [
                                {
                                    "title": "New Tariff Requirements 2025 Factsheet - U.S. Customs and Border Protection",
                                    "link": "https://www.cbp.gov/document/fact-sheets/new-tariff-requirements-2025-factsheet",
                                    "snippet": "The New Tariff Requirements 2025 Factsheet will provide information on Executive Orders and Proclamations that have imposed new tariffs on goods imported into the United States pursuant to the International Emergency Economic Powers Act (IEEPA) and Section 232 of the Trade Expansion Act of 1962. Attachment"
                                },
                                {
                                    "title": "Analysis: US tariffs could make Europe 'Great Again' by ... - CNN",
                                    "link": "https://www.cnn.com/2025/05/02/economy/europe-lower-inflation-us-tariffs-analysis-intl",
                                    "snippet": "President Donald Trump might want a new, \"America First\" world, but in the race to control inflation the United States may actually come last. While his tariff hikes are widely expected to ..."
                                },
                                {
                                    "title": "Trump imposes sweeping 25% steel and aluminum tariffs. Canada and ... - CNN",
                                    "link": "https://www.cnn.com/2025/03/12/economy/trump-steel-aluminum-tariffs-hnk-intl/index.html",
                                    "snippet": "Hours before enacting the latest tariffs, Trump reversed a threat to double the rate on steel and aluminum from Canada, the US's top source of imports for the metals. Instead, steel and aluminum ..."
                                },
                                {
                                    "title": "2025 U.S. Tariffs Update - New Trade Policies & Ecommerce Impact ...",
                                    "link": "https://zonos.com/docs/guides/2025-us-tariff-changes",
                                    "snippet": "February 24, 2025. Announced - Tariffs on Canadian- and Mexican-made goods to resume: President Trump confirmed that the previously paused tariffs on goods made in Canada and Mexico will proceed on March 4, 2025. This includes a 25% tariff on most Canadian- and Mexican-made products and a 10% tariff on Canadian energy imports."
                                }
                            ],
                            "exa_output": [
                                {
                                    "highlights": [
                                        "On 3 February 2025, the United States reached agreements with Canada and Mexico to pause tariffs on imports from those countries in exchange for actions on border security, illegal drugs, and immigration. As a result of these steps, tariffs of 25% on imports from Mexico, 10% on certain energy and critical mineral imports from Canada, and 25% on all remaining imports from Canada will be paused for 30 days, through 12:01 am ET on 4 March 2025. Retaliatory tariffs and other retaliatory measures by Canada and Mexico are also on hold through that date. Companies and investors with interests in North America should use this pause in tariffs to review their supply chains, investments, and business plans. There is particular urgency for those companies with cross-border operations and for those dealing in energy and energy products from Canada."
                                    ],
                                    "url": "https://www.jdsupra.com/legalnews/us-tariff-and-trade-update-temporary-9113683/"
                                },
                                {
                                    "highlights": [
                                        "\\\\* Semiconductors: Tariffs will increase from 25% to 50% by 2025, the White House said, citing China's huge share in new semiconductor wafers coming online and a spike in prices during the pandemic. \\\\* Electric Vehicles: Tariffs will increase from 25% to 100% in 2024 (on top of a separate 2.5% tariff), the White House said, citing \"extensive subsidies and non-market practices leading to substantial risks of overcapacity. \" The U.S. Trade Representative's Office said plug-in hybrid electric vehicles will be covered by the new tariffs but not hybrid vehicles. \\\\* Batteries, Battery Components and Parts: Tariffs on lithium-ion EV batteries will increase from 7.5% to 25% in 2024, while the tariff rate on lithium-ion non-EV batteries will increase from 7.5% to 25% in 2026. Tariff rates on battery parts will increase from 7.5% to 25% in 2024"
                                    ],
                                    "url": "https://www.reuters.com/world/what-are-bidens-new-tariffs-china-goods-2024-05-14/"
                                },
                                {
                                    "highlights": [
                                        "The import tax on Chinese solar cells will double, from 25% to 50%. And tariffs on some Chinese steel and aluminum imports will increase more than three-fold, from 7.5% today up to 25%. Some items, like batteries and natural graphite, will have longer phase-in periods for tariffs. The White House said this is partly to give the U.S. manufacturing sector time to scale up to a point where enough batteries are being produced domestically to meet consumer demand. “The U.S.’s escalation of Section 301 tariffs contradicts President Biden’s commitments not to suppress or contain China’s development and not to seek decoupling from China,” a spokesperson for the Ministry of Commerce said in a statement."
                                    ],
                                    "url": "https://www.cnbc.com/2024/05/14/biden-raises-china-tariffs-on-evs-solar-panels-batteries-.html"
                                },
                                {
                                    "highlights": [
                                        "No member firm has any authority to obligate or bind KPMG International or any other member firm vis-à-vis third parties, nor does KPMG International have any such authority to obligate or bind any member firm. The information contained herein is of a general nature and is not intended to address the circumstances of any particular individual or entity. Although we endeavor to provide accurate and timely information, there can be no guarantee that such information is accurate as of the date it is received or that it will continue to be accurate in the future. No one should act on such information without appropriate professional advice after a thorough examination of the particular situation. For more information, contact KPMG's Federal Tax Legislative and Regulatory Services Group at: + 1 202 533 3712, 1801 K Street NW, Washington, DC 20006."
                                    ],
                                    "url": "https://kpmg.com/us/en/taxnewsflash/news/2025/03/united-states-duty-free-de-minimis-treatment-canada-mexico.html"
                                },
                                {
                                    "highlights": [
                                        "Specific U.S. Harmonized Tariff Schedule classifications impacted will be identified in a forthcoming _Federal Register_ notice, but no product exemptions are identified in the February 1st actions. In retaliation for these new actions, also on February 1st, Canadian Prime Minister Justin Trudeau and Mexican President Claudia Sheinbaum announced plans to implement retaliatory trade measures against U.S. exports to those countries. If your business may be impacted by these actions, please reach out to [Deanna Okun](mailto:dtokun@polsinelli.com) or [Lydia Pardini](mailto:lpardini@polsinelli.com). The Polsinelli International Trade team will be keeping the full update link current with the latest announcements regarding these actions. - 25% tariffs on all goods from Canada, except for “energy resources” from Canada."
                                    ],
                                    "url": "https://www.polsinelli.com/publications/new-tariffs-on-u-s-imports-from-canada-mexico-and-china"
                                }
                            ],
                            "tavily_output": {
                                "results": [
                                    {
                                        "title": "U.S. Companies Dive Into Cost-Cutting as Tariff Uncertainty Swirls - WSJ",
                                        "url": "https://www.wsj.com/business/tariffs-companies-spending-2025-0c84b037",
                                        "content": "CEOs are pausing travel, delaying construction projects and slowing hiring in response to tariffs and cloudy economic forecasts: \"Control the controllables.\""
                                    },
                                    {
                                        "title": "The US Stock Market's Tariff Exposure Is About to Be Laid Bare",
                                        "url": "https://www.bloomberg.com/news/articles/2025-04-25/the-us-stock-market-s-tariff-exposure-is-about-to-be-laid-bare",
                                        "content": "President Donald Trump's raft of tariffs is set to expose just how vulnerable the US stock market is to a trade war.. The track record of S&P 500 Index companies over the past two decades"
                                    },
                                    {
                                        "title": "T-Day Is Coming. What Will Tariffs Do To The Economy? - Investopedia",
                                        "url": "https://www.investopedia.com/t-day-is-coming-what-will-tariffs-do-to-the-economy-11685581",
                                        "content": "Many forecasts expect the tariffs to drive inflation by pushing up consumer prices while also slowing down growth, raising risks of an economic double-whammy known as \"stagflation.\""
                                    }
                                ]
                            }
                        }
                    }
                ],
                "header": {
                    "title": "American Tariffs Today: Current Status and Impact",
                    "summary": "This report provides an overview of the current status of American tariffs, including recent developments and their practical impact. The key points covered include the current landscape of tariff policies, the immediate economic effects, and the latest changes within the last 6-12 months."
                },
                "sections": {
                    "sections": [
                        {
                            "section_id": "b744e004-93d0-4c82-80fc-e947e618ca14",
                            "name": "Introduction to American Tariffs",
                            "description": "Overview of the current American tariff landscape",
                            "research": True,
                            "content": "Recent policies and rates, including any significant changes within the last year"
                        },
                        {
                            "section_id": "d2e33319-9132-44c6-a44c-a138dca9573b",
                            "name": "Latest Tariff Developments and Updates",
                            "description": "Recent changes and developments in American tariffs",
                            "research": True,
                            "content": "Changes within the past 6-12 months, including new policies and their effects"
                        },
                        {
                            "section_id": "bb6b474e-3e90-43a6-a2ed-b7ce9f8c885d",
                            "name": "Economic Impact of Current Tariffs",
                            "description": "Analysis of the current economic impact of American tariffs",
                            "research": True,
                            "content": "Current effects on industries and trade, including any data on job losses or gains, and changes in trade volumes"
                        },
                        {
                            "section_id": "4ff8ad8f-43ef-49e1-bf8c-654a670ccc2b",
                            "name": "Outlook and Future of American Tariffs",
                            "description": "Predicted near-future developments and changes in American tariffs",
                            "research": True,
                            "content": "Expected changes in tariff policies, potential impacts on the economy, and possible responses from trading partners"
                        }
                    ]
                },
                "footer": {
                    "conclusion": "## Conclusion\n\nIn summary, the current status of American tariffs is marked by significant recent developments and ongoing changes. The latest policies and rates have undergone substantial adjustments within the last year, with notable updates in the past 6-12 months introducing new policies that are affecting various sectors of the economy.\n\nThe economic impact of these tariffs is multifaceted, with both positive and negative effects on different industries and trade volumes. While some sectors have experienced job gains and increased trade, others have faced challenges, including job losses and decreased trade volumes. The most current data highlights the complexity of these effects, underscoring the need for ongoing analysis and adaptation.\n\nLooking ahead, the outlook for American tariffs suggests further changes and potential shifts in policy. Expected adjustments in tariff policies could have profound impacts on the economy, prompting varied responses from trading partners. As the global trade landscape continues to evolve, it is crucial to prioritize the most recent information and developments in American tariffs to understand their practical implications and navigate the future of international trade effectively.\n\n**Key Takeaways:**\n1. **Recent Policy Changes:** Significant adjustments have been made to American tariffs within the last year, including new policies implemented in the past 6-12 months.\n2. **Economic Impact:** The current tariffs have a varied impact on the economy, with both positive and negative effects on industries and trade.\n3. **Future Outlook:** The future of American tariffs is expected to involve further policy changes, which could substantially impact the economy and prompt responses from trading partners.\n\nBy focusing on the latest developments and their practical implications, stakeholders can better understand the current status and future trajectory of American tariffs, facilitating informed decision-making in the ever-changing landscape of international trade."
                },
                "references":None,
                "markdown": None
            },
        config={
            "callbacks":[langfuse_handler],
            "configurable":{"thread_id":"abc123"}
        }
    ):
        writer_state= state
        print(writer_state)
    print("Final Writer State:",writer_state)
    
    
asyncio.run(main())
