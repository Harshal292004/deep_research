from utilities.states.tool_state import TavilyQuery,DuckDuckGoQuery, ExaQuery
from components.tools import tavily_search,duckduckgo_search, exa_search
import asyncio


async def main():
    duckduckgo_query=DuckDuckGoQuery(query='current American tariffs', max_results=3)
    d_output=await  duckduckgo_search(input=duckduckgo_query)
    print(f"DuckDuck output : {type(d_output)} | Content: {d_output} ")

exa_query = ExaQuery(
    query="OpenAI GPT-4 architecture",
    num_results=10,
    start_published_date="2023-01-01",
    end_published_date="2023-12-31",
    category="research paper"
)

print(exa_search(input= exa_query))

from utilities.states.report_state import WriterState

dict_= {
            "query": "What is the current status of the american tariffs?",
            "type_of_query": "factual_query",
            "outputs": [
                {
                    "section_id": "77148be2-01c2-4e0c-b6cd-b445b4557deb",
                    "output_state": {
                        "duckduckgo_output": [
                            {
                                "title": "Trump 2.0 tariff tracker | Trade Compliance Resource Hub",
                                "link": "https://www.tradecomplianceresourcehub.com/2025/04/29/trump-2-0-tariff-tracker/",
                                "snippet": "Reciprocal tariff exemption: imports not subject to reciprocal tariffs at this time: Bosnia and Herzegovina: Reciprocal tariff: Delayed until July 9 (effective Apr. 10, 2025) 36%: All products (see exceptions below) Botswana: Reciprocal tariff: Delayed until July 9 (effective Apr. 10, 2025) 38%: All products (see exceptions below) BRICS 2"
                            },
                            {
                                "title": "See what tariffs are currently in place, who's impacted by trade war",
                                "link": "https://www.usatoday.com/story/graphics/2025/04/10/current-trump-tariffs-map/83026822007/",
                                "snippet": "The U.S. economy has been riding a financial roller coaster driven by President Donald Trump's trade war and his April 2 announcement of tariffs on imports to all U.S. trading partners. Trump ..."
                            },
                            {
                                "title": "U.S. Tariff Rates by Country - Trump Reciprocal Tariffs, April 2025",
                                "link": "https://passportglobal.com/us-tariff-rates-by-country-2025/",
                                "snippet": "Instead, effective April 10, 2025, a flat 10% tariff applies to imports from all countries. China and Hong Kong are the exception: imports from these countries are subject to a 125% reciprocal tariff, in addition to other existing tariffs, including the 20% rate imposed in March."
                            },
                            {
                                "title": "Tariff timeline: Tracking the evolution of Trump's trade war",
                                "link": "https://www.usatoday.com/story/graphics/2025/03/28/trump-tariff-tracker-timeline/82367214007/",
                                "snippet": "See the current status and details on how it unfolded. ... announced 25% reciprocal tariffs on steel products and additional American products, and the EU plans to slap a 50% tariff on American ..."
                            }
                        ],
                        "exa_output": [
                            {
                                "highlights": [
                                    "\\\\* Certain steel and aluminum products: Tariffs more than triple on some these products, [estimated earlier](https://www.reuters.com/world/us/biden-call-higher-tariffs-chinese-metals-steel-city-pittsburgh-2024-04-17/) at least $1 billion in goods, from the current range of zero to 7.5% to 25% in 2024. \\\\* Semiconductors: Tariffs will increase from 25% to 50% by 2025, the White House said, citing China's huge share in new semiconductor wafers coming online and a spike in prices during the pandemic. \\\\* Electric Vehicles: Tariffs will increase from 25% to 100% in 2024 (on top of a separate 2.5% tariff), the White House said, citing \"extensive subsidies and non-market practices leading to substantial risks of overcapacity. \" The U.S. Trade Representative's Office said plug-in hybrid electric vehicles will be covered by the new tariffs but not hybrid vehicles. \\\\* Batteries, Battery Components and Parts: Tariffs on lithium-ion EV batteries will increase from 7.5% to 25% in 2024, while the tariff rate on lithium-ion non-EV batteries will increase from 7.5% to 25% in 2026."
                                ],
                                "url": "https://www.reuters.com/world/what-are-bidens-new-tariffs-china-goods-2024-05-14/"
                            },
                            {
                                "highlights": [
                                    "“We’re going to see a revival and increased attention on tariffs in 2024 from the US,” Scott Kennedy, a chair in Chinese business and economics at the Centre for Strategic and International Studies (CSIS), told a virtual panel discussion organised by the Washington think tank. Imposed since the Donald Trump administration, average US tariffs on imports from China remain elevated at 19.3 per cent. The US also has 247 anti-dumping and countervailing duty measures in place against Chinese goods, including steel, chemicals, machinery and automobiles, Kennedy added. But a stiff 27.5 per cent tariff – in place since Trump’s presidency – along with US President Joe Biden’s signature legislation, the Inflation Reduction Act, that provides subsidies for domestic electric vehicle manufacturers, have largely kept Chinese EVs at bay in the US market. Still, US reliance on imports of Chinese-made lithium batteries has continued to rise in recent years."
                                ],
                                "url": "https://www.scmp.com/news/china/diplomacy/article/3248691/us-tariffs-chinese-imports-might-increase-2024-analysts-say"
                            }
                        ],
                        "tavily_output": {
                            "results": [
                                {
                                    "title": "Trump Planning to Ease Automotive Tariffs, Says U.S. Commerce Secretary - Car and Driver",
                                    "url": "https://www.caranddriver.com/news/a64619872/trump-easing-automotive-tariffs/",
                                    "content": "UPDATE 4/29/25 4:45 p.m.: This story has been updated to confirm that President Trump signed two executive orders on Tuesday that walk back some portions of the tariffs he previously imposed on the automotive industry. The change means that automakers won't pay additional tariffs, namely on steel and aluminum, in addition to the blanket 25 percent levy for cars built in foreign countries. What to Know When Buying a Car in Tariff Times Tariffs May Mean 2M Fewer Car Sales This Year Automakers' Tariff Response: What We Know So Far Report: Tariffs Kill the Volvo S90 Sedan in U.S. Canada Adds 25% Tariffs to U.S.-Sourced Cars"
                                },
                                {
                                    "title": "Facing pressure, Trump scales back tariffs for US automakers - Electrek",
                                    "url": "https://electrek.co/2025/04/29/trump-scales-back-tariffs-us-automakers/",
                                    "content": "Donald Trump signed two executive orders today that walked back parts of tariffs he previously imposed on US automakers ahead of a rally in Michigan to mark his first 100 days in office. American Automotive Policy Council (AAPC) president Matt Blunt today said in response to the executive orders, “American Automakers Ford, GM, and Stellantis appreciate the administration’s clarification that tariffs will not be layered on top of the existing Section 232 tariffs on autos and auto parts. American Automakers Ford, GM, and Stellantis appreciate the administration’s clarification that tariffs will not be layered on top of the existing Section 232 tariffs on autos and auto parts."
                                }
                            ]
                        }
                    }
                },
                {
                    "section_id": "51d80331-aa5d-4db0-8b00-a08bd984d9b0",
                    "output_state": {
                        "duckduckgo_output": [
                            {
                                "title": "Trump 2.0 tariff tracker | Trade Compliance Resource Hub",
                                "link": "https://www.tradecomplianceresourcehub.com/2025/04/29/trump-2-0-tariff-tracker/",
                                "snippet": "Reciprocal tariff exemption: imports not subject to reciprocal tariffs at this time: Bosnia and Herzegovina: Reciprocal tariff: Delayed until July 9 (effective Apr. 10, 2025) 36%: All products (see exceptions below) Botswana: Reciprocal tariff: Delayed until July 9 (effective Apr. 10, 2025) 38%: All products (see exceptions below) BRICS 2"
                            },
                            {
                                "title": "See what tariffs are currently in place, who's impacted by trade war",
                                "link": "https://www.usatoday.com/story/graphics/2025/04/10/current-trump-tariffs-map/83026822007/",
                                "snippet": "The U.S. economy has been riding a financial roller coaster driven by President Donald Trump's trade war and his April 2 announcement of tariffs on imports to all U.S. trading partners. Trump ..."
                            },
                            {
                                "title": "U.S. Tariff Rates by Country - Trump Reciprocal Tariffs, April 2025",
                                "link": "https://passportglobal.com/us-tariff-rates-by-country-2025/",
                                "snippet": "Instead, effective April 10, 2025, a flat 10% tariff applies to imports from all countries. China and Hong Kong are the exception: imports from these countries are subject to a 125% reciprocal tariff, in addition to other existing tariffs, including the 20% rate imposed in March."
                            },
                            {
                                "title": "Tariff timeline: Tracking the evolution of Trump's trade war",
                                "link": "https://www.usatoday.com/story/graphics/2025/03/28/trump-tariff-tracker-timeline/82367214007/",
                                "snippet": "See the current status and details on how it unfolded. ... announced 25% reciprocal tariffs on steel products and additional American products, and the EU plans to slap a 50% tariff on American ..."
                            }
                        ],
                        "exa_output": [
                            {
                                "highlights": [
                                    "negative impact on consumer demand, our operating results and liquidity. • Our business is subject to extensive government regulation, which may result in increases in our costs, disruptions to our operations, limits on our operating flexibility, reductions in the demand for air travel, and • We operate a global business with international operations that are subject to economic and political instability and have been, and in the future may continue to be, adversely affected by numerous events, circumstances or"
                                ],
                                "url": "https://www.sec.gov/Archives/edgar/data/6201/000119312524114062/d636721dars.pdf"
                            },
                            {
                                "highlights": [
                                    "Domestic capacity in 2021 was down 14.5% while international capacity was down 44.9% as compared to 2019. While demand for domestic and short-haul international markets has largely recovered to 2019 levels, uncertainty remains regarding the timing of a full recovery. We will continue to match our forward capacity with observed booking trends for future travel and make further adjustments to our capacity as needed. COVID-19 has been declared a global health pandemic by the World Health Organization. COVID-19 has surfaced in nearly all regions of the world, which has driven the implementation of significant, government-imposed measures to prevent or reduce its spread, including travel restrictions, testing regimes, closing of borders, “stay at home” orders and business closures."
                                ],
                                "url": "https://www.sec.gov/Archives/edgar/data/6201/000000620122000026/aal-20211231.htm"
                            }
                        ],
                        "tavily_output": {
                            "results": [
                                {
                                    "title": "Trump's Tariffs: How Do They Work? Who Pays? - Bloomberg",
                                    "url": "https://www.bloomberg.com/explainers/trump-s-tariffs-explained",
                                    "content": "Trump’s tariff orders on imports from Canada, Mexico and China — the three largest trading partners of the US, which together accounted for about 40% of all merchandise trade last year — are intended to address what he calls a “threat to the safety and security of Americans, including the public health crisis of deaths due to the use of fentanyl.” A decision to twice delay the tariffs on some imports from Mexico and Canada came after their governments agreed to step up efforts to address illegal migration and drug trafficking at the US border, and Trump said at the time he was satisfied that progress was being made."
                                },
                                {
                                    "title": "The Impact Of Trump's Tariffs: Who Will Benefit And What ... - Forbes",
                                    "url": "https://www.forbes.com/sites/daniellechemtob/2025/02/12/how-will-tariffs-impact-you-heres-what-to-know-about-trumps-plans/",
                                    "content": "The Impact Of Trump’s Tariffs: Who Will Benefit And What Consumers Can Expect From reciprocal tariffs to a focus on Mexico and Canada, economist forecasts and recent history both indicate that Trump’s trade policies will increase prices for American consumers. Here’s a rundown on the history and impacts of recent tariffs, Trump’s proposals and what to expect when it comes to increased costs. Trump’s China tariffs are expected to impact a wide variety of consumer goods, from electronics to toys and shoes. If Trump were to implement what’s called “country-level reciprocity,” or the same average tariff that our trading partners place on U.S. goods, the U.S. would see a weighted average tariff rate of 4.8%, Deutsche Bank economists estimated."
                                },
                                {
                                    "title": "Tariffs Will Hit All U.S. Imports. Price Hikes for These Items May ...",
                                    "url": "https://www.wsj.com/economy/trade/tariffs-will-hit-all-u-s-imports-price-hikes-for-these-items-may-surprise-you-dcb92d42",
                                    "content": "President Trump's announcement of 10% across-the-board tariffs on all imports to the U.S. and even higher rates for some nations' goods will likely affect the prices of everything from small"
                                }
                            ]
                        }
                    }
                },
                {
                    "section_id": "c95b24b9-2104-4411-9554-9ff8247738b7",
                    "output_state": {
                        "duckduckgo_output": [
                            {
                                "title": "See what tariffs are currently in place, who's impacted by trade war",
                                "link": "https://www.usatoday.com/story/graphics/2025/04/10/current-trump-tariffs-map/83026822007/",
                                "snippet": "The U.S. economy has been riding a financial roller coaster driven by President Donald Trump's trade war and his April 2 announcement of tariffs on imports to all U.S. trading partners. Trump ..."
                            },
                            {
                                "title": "Trump 2.0 tariff tracker | Trade Compliance Resource Hub",
                                "link": "https://www.tradecomplianceresourcehub.com/2025/04/29/trump-2-0-tariff-tracker/",
                                "snippet": "Reciprocal tariff exemption: imports not subject to reciprocal tariffs at this time: Bosnia and Herzegovina: Reciprocal tariff: Delayed until July 9 (effective Apr. 10, 2025) 36%: All products (see exceptions below) Botswana: Reciprocal tariff: Delayed until July 9 (effective Apr. 10, 2025) 38%: All products (see exceptions below) BRICS 2"
                            },
                            {
                                "title": "Tariff Tracker: Where Do President Trump's Trade Proposals Stand?",
                                "link": "https://www.investopedia.com/tariff-tracker-where-do-president-trump-trade-proposals-stand-11702803",
                                "snippet": "China: The U.S. and China have gotten into a tit-for-tat trade war, resulting in a total of 145% tariff on Chinese goods coming into the U.S. China has levied import taxes on American goods at a ..."
                            },
                            {
                                "title": "Tariff timeline: Tracking the evolution of Trump's trade war",
                                "link": "https://www.usatoday.com/story/graphics/2025/03/28/trump-tariff-tracker-timeline/82367214007/",
                                "snippet": "See the current status and details on how it unfolded. ... announced 25% reciprocal tariffs on steel products and additional American products, and the EU plans to slap a 50% tariff on American ..."
                            }
                        ],
                        "exa_output": [
                            {
                                "highlights": [
                                    "The expected tariffs are part of the Biden administration's broader strategy to protect the U.S. against supply shortages seen during the pandemic that left hospitals scrambling to find critical equipment, the sources said. In December, the United States Trade Representative announced a further extension of China-related \"Section 301\" tariff exclusions until May 31. The American Medical Manufacturers Association has called for these exclusions to be revoked, arguing they are no longer needed to deal with a COVID-19 emergency. The association says American manufacturers need the chance to compete with imports on a more level playing field. MORE TARIFFS ON METAL PRODUCTS?"
                                ],
                                "url": "https://www.reuters.com/world/how-hard-will-new-biden-tariffs-hit-china-2024-05-13/"
                            },
                            {
                                "highlights": [
                                    "“Tariffs solve one half of the equation. The other half is how to ignite a mind-set of innovation, intensity and ambition among domestic automakers,” he said. More than a decade after Wen Jiabao, then Chinese prime minister, warned that China’s growth was “unbalanced, uncoordinated and unsustainable,” its leaders continue to prioritize manufacturing over greater consumer buying power. China spends more on industrial policies to shape its economy than it does on defense, said a 2022 report by the Center for Strategic and International Studies. In dollar terms, China spends more than twice as much as the United States, according to the report, which was funded by the State Department."
                                ],
                                "url": "https://www.washingtonpost.com/business/2024/05/14/biden-china-tariff-ev-solar/"
                            }
                        ],
                        "tavily_output": {
                            "results": [
                                {
                                    "title": "Trump tariffs live updates: China says 'door is open' to trade talks ...",
                                    "url": "https://finance.yahoo.com/news/live/trump-tariffs-live-updates-trump-threatens-additional-tariffs-on-china-markets-remain-jittery-191201930.html",
                                    "content": "In a post on X, Daniel Tannebaum shed light on how tariffs are quietly squeezing American consumers. Tannebaum shared a personal anecdote: The swimsuit cost $198, with $20 in shipping — but the"
                                },
                                {
                                    "title": "Trump Tariffs: Track Targeted Goods and Economic Impact Worldwide",
                                    "url": "https://www.bloomberg.com/graphics/trump-tariffs-tracker/",
                                    "content": "These goods are currently excluded from the \"reciprocal\" tariffs that were first announced on April 2, which are currently the subject of negotiations between the US and trade partners across"
                                }
                            ]
                        }
                    }
                }
            ],
            "header": {
                "title": "Current Status of American Tariffs",
                "summary": "The report will cover the definition and key characteristics of American tariffs, their scientific basis and underlying principles, real-world applications, and common misconceptions surrounding the topic."
            },
            "sections": {
                "sections": [
                    {
                        "section_id": "77148be2-01c2-4e0c-b6cd-b445b4557deb",
                        "name": "Definition & Core Concept",
                        "description": "Explanation of American tariffs, including their definition, history, and key characteristics",
                        "research": True,
                        "content": "The section will delve into the fundamentals of American tariffs, exploring their purpose, types, and evolution over time"
                    },
                    {
                        "section_id": "51d80331-aa5d-4db0-8b00-a08bd984d9b0",
                        "name": "Scientific Basis",
                        "description": "Underlying principles and economic theories behind American tariffs",
                        "research": True,
                        "content": "This section will examine the economic and political foundations of American tariffs, including trade policies and international agreements"
                    },
                    {
                        "section_id": "c95b24b9-2104-4411-9554-9ff8247738b7",
                        "name": "Real-World Applications",
                        "description": "Impact of American tariffs on various industries and the global economy",
                        "research": True,
                        "content": "The section will discuss the practical effects of American tariffs on different sectors, such as manufacturing, agriculture, and services, as well as their influence on global trade patterns"
                    },
                    {
                        "section_id": "03e6aa3e-500f-4578-bf45-7b08ddb3022d",
                        "name": "Misconceptions & Clarifications",
                        "description": "Addressing common misconceptions and providing clarity on the current status of American tariffs",
                        "research": False,
                        "content": "This final section will aim to dispel common myths and misconceptions surrounding American tariffs, offering a balanced view of their current status and future prospects"
                    }
                ]
            },
            "footer": {
                "conclusion": "## Conclusion\n\n### Key Insight Summary:\nAmerican tariffs have a complex history, with their definition, purpose, and characteristics evolving over time. They are designed to protect domestic industries, raise revenue, and influence trade policies. The tariffs are grounded in economic theories and are shaped by international agreements and trade policies. In practice, American tariffs have significant impacts on various industries, including manufacturing, agriculture, and services, and play a crucial role in global trade patterns. Common misconceptions about tariffs have been clarified, providing a clearer understanding of their current status and implications.\n\n### Final Thoughts:\nThe current status of American tariffs reflects a dynamic and often contentious aspect of international trade and economic policy. Understanding the fundamentals, scientific basis, and real-world applications of tariffs is essential for navigating the complexities of global trade. As the global economy continues to evolve, the role and impact of American tariffs will likely remain a critical issue, influencing not just the US economy but also international trade relations and global economic stability.\n\n### Implications:\nThe implications of American tariffs are far-reaching, affecting not just the United States but also its trading partners and the global economy as a whole. As trade policies continue to shift, it's crucial for policymakers, businesses, and individuals to stay informed about the current status and future directions of American tariffs. This knowledge can help in making informed decisions, mitigating potential risks, and capitalizing on opportunities arising from changes in tariff policies. Furthermore, understanding the economic and political underpinnings of tariffs can provide insights into broader geopolitical and economic trends, highlighting the interconnectedness of the world's economies and the importance of balanced and fair trade practices."
            }
        }


output=WriterState(**dict_)


print(output)
