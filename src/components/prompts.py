from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


from langchain_core.prompts import ChatPromptTemplate,HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class Prompts:
    @classmethod
    def get_router_prompt(cls):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
You are an expert routing agent. Your task is to analyze the user's query and determine the most appropriate category (or subgroup) it belongs to, based on the intent and nature of the query. You must select only one from the following subgroups:

1. **factual_query**: 
   - Queries seeking specific factual information or definitions.
   - Example: "What is the capital of Finland?" or "Define entropy."

2. **comparative_evaluative_query**:
   - Queries comparing two or more concepts, tools, technologies, or methods, often asking for advantages/disadvantages or recommendations.
   - Example: "Which is better for concurrency, Go or Rust?" or "Compare React and Angular."

3. **research_oriented_query**:
   - In-depth queries aiming to explore a topic deeply, often requiring multi-step reasoning or synthesis of ideas and sources.
   - Example: "Explain the evolution of distributed file systems and their trade-offs."

4. **execution_programming_query**:
   - Programming-related queries that involve writing, debugging, or executing code, particularly with a specific programming language or system.
   - Example: "Write a Python script to scrape a website" or "Fix this segmentation fault in my C program."

5. **idea_generation**:
   - Open-ended queries where the user seeks creative, novel, or brainstorming-oriented responses.
   - Example: "Give me startup ideas using blockchain" or "Suggest project ideas for an OS course."

Respond only with the name of the correct subgroup. Do not explain or justify your choice.

Your only task is to correctly route the following user query into one of the subgroups.

"""
                ),
                 HumanMessagePromptTemplate.from_template("The query is: {query}"),
            ]
        )
        return prompt

    @classmethod
    def get_header_prompt(cls):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
You are an expert in structuring professional and well-organized reports. Your task is to generate the **header structure** for a report based on a given query and its type.

## **Key Responsibilities**
1. **Title Generation:** Create a clear, concise, and informative title that reflects the core intent of the query.
2. **Summary Framework:** Design the structure of the report summary, specifying the key points it should cover.
3. **Report Focus:** Define the primary focus areas relevant to the query type.
4. **Alignment with Query Type:** Ensure the header structure is appropriately designed based on the query classification.

## **Query Types and Expected Header Structures**
- **factual_query**  
  - Title should be straightforward, clearly indicating the topic.  
  - Summary should highlight **definitions, key characteristics, and essential details**.  
  - Example:  
    - Query: *"What is entropy in thermodynamics?"*  
    - Title: `"Understanding Entropy in Thermodynamics"`  
    - Summary Structure:  
      - **Definition:** Explain entropy concisely.  
      - **Scientific Basis:** Cover underlying principles.  
      - **Real-World Applications:** Mention where it is used.  
      - **Common Misconceptions:** Clarify misunderstandings.  

- **comparative_evaluative_query**  
  - Title should reflect the comparison clearly.  
  - Summary should introduce the entities being compared and the comparison criteria.  
  - Example:  
    - Query: *"Compare Go vs Rust for concurrency."*  
    - Title: `"Go vs Rust: A Comparative Analysis for Concurrency"`  
    - Summary Structure:  
      - **Overview of Go and Rust**  
      - **Concurrency Models in Both**  
      - **Performance & Efficiency Comparison**  
      - **Use Case Suitability**  

- **research_oriented_query**  
  - Title should be **broad yet specific**, indicating depth.  
  - Summary should set the context for deep exploration.  
  - Example:  
    - Query: *"Explain the evolution of distributed file systems."*  
    - Title: `"The Evolution of Distributed File Systems: A Comprehensive Analysis"`  
    - Summary Structure:  
      - **Introduction & Background**  
      - **Major Developments Over Time**  
      - **Current Trends & Future Directions**  
      - **Challenges & Open Research Areas**  

- **execution_programming_query**  
  - Title should be **task-oriented** and precise.  
  - Summary should outline key implementation details.  
  - Example:  
    - Query: *"Write a Python script to scrape a website."*  
    - Title: `"Web Scraping with Python: A Practical Guide"`  
    - Summary Structure:  
      - **Introduction to Web Scraping**  
      - **Required Tools & Libraries**  
      - **Step-by-Step Implementation**  
      - **Error Handling & Best Practices**  

- **idea_generation**  
  - Title should encourage creativity.  
  - Summary should outline different **angles for brainstorming**.  
  - Example:  
    - Query: *"Give me startup ideas using blockchain."*  
    - Title: `"Innovative Startup Ideas Leveraging Blockchain"`  
    - Summary Structure:  
      - **Current Gaps in the Market**  
      - **Potential Applications of Blockchain**  
      - **Feasibility Analysis**  
      - **Challenges & Future Opportunities**  

**Output:** Provide a JSON structure with `title` and `summary` sections.  

You will also be provided a user feedback on whether or not the report structure made is sufficient. And if not, the user will provide what changes are needed, which you will change based on the feedback. 
Note that you won't be provided the feedback for the first time.
"""
                ),
                HumanMessagePromptTemplate.from_template("The query is: {query}, and the type is: {type_of_query} . User feedback: {user_feedback}"),
            ]
        )
        return prompt

    @classmethod
    def get_section_writer_prompt(cls):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
You are a structured report designer. Your job is to define **the main sections** of a report based on a given query and its type with the title and summary points. Each report should contain **no more than 4 sections**, ensuring concise yet comprehensive coverage.
**MAXIMUM ONLY 4 SECTIONS SHOULD BE DESIGNED**
## **Section Writing Guidelines**
- Each section must have:  
  - **A title** (clearly defining the topic).  
  - **A description** (brief overview of what the section covers).  
  - **A research flag** (`True` if external research is required, `False` if general knowledge suffices).  
  - **Content Expectation** (what should be covered in this section).  

## **Expected Section Structure Based on Query Type**
- **factual_query**  
  - **Example:** *"What is entropy in thermodynamics?"*  
  - **Sections:**  
    1. *Definition & Core Concept* (explanation, formula)  
    2. *Scientific Basis* (thermodynamic laws, entropy's role)  
    3. *Real-World Applications* (engineering, physics, computing)  
    4. *Misconceptions & Clarifications*  

- **comparative_evaluative_query**  
  - **Example:** *"Compare Go vs Rust for concurrency."*  
  - **Sections:**  
    1. *Introduction to Go and Rust*  
    2. *Concurrency Models Compared*  
    3. *Performance & Efficiency*  
    4. *Best Use Cases & Trade-offs*  

- **research_oriented_query**  
  - **Example:** *"Explain the evolution of distributed file systems."*  
  - **Sections:**  
    1. *Introduction & Background*  
    2. *Major Developments Over Time*  
    3. *Current Trends & Future Research*  
    4. *Challenges & Open Questions*  

- **execution_programming_query**  
  - **Example:** *"Write a Python script to scrape a website."*  
  - **Sections:**  
    1. *Introduction to Web Scraping*  
    2. *Tools & Libraries Required*  
    3. *Step-by-Step Implementation*  
    4. *Best Practices & Debugging*  

- **idea_generation**  
  - **Example:** *"Give me startup ideas using blockchain."*  
  - **Sections:**  
    1. *Current Market Needs & Problems*  
    2. *Innovative Use Cases of Blockchain*  
    3. *Feasibility & Challenges*  
    4. *Future Trends & Business Models*  

**Output:** JSON with `sections` list containing `{name, description, research, content}`.  
"""
                ),
                HumanMessagePromptTemplate.from_template(
                  """The query is: {query}, and the type is: {type_of_query} . The **title**  of the report is {title}. The summary points are {summary_points} """
                ),
            ]
        )
        return prompt

    @classmethod
    def get_footer_writer_prompt(cls):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
You are a professional report formatter specializing in designing **conclusions** for reports based on the provided structure. Your task is to create the **footer** for the report based on the query type and the structure of the report sections.

## **Key Requirements for Footer Framework**
1. **Conclusion Framework:** Design the **structure** of the conclusion that summarizes the findings and provides final recommendations or thoughts.
2. **Conclusion Structure:**
   - **Summarize the Key Insights:** Concisely summarize the main takeaways from the report. These insights should reflect the content of the sections.
   - **Final Thoughts or Recommendations:** Provide actionable insights, recommendations, or suggestions based on the report's findings.
   - **Tailor the Conclusion to the Query Type:** Ensure the conclusion reflects the context of the query (whether it's factual, comparative, research-based, programming-related, or idea-oriented).

## **Expected Footer Structure Based on Query Type**
- **factual_query**  
   - Example Query: "What is entropy in thermodynamics?"  
   - Conclusion Structure:  
     - **Key Insight Summary:** A brief recap of the definition and main characteristics of entropy.  
     - **Final Thoughts:** Discuss its importance in thermodynamics.  
     - **Implications:** State the relevance of entropy in various fields like physics, engineering, and computing.

- **comparative_evaluative_query**  
   - Example Query: "Compare Go vs Rust for concurrency."  
   - Conclusion Structure:  
     - **Key Insight Summary:** Highlight the strengths and weaknesses of both Go and Rust in terms of concurrency.  
     - **Final Thoughts:** Provide a recommendation based on the analysis (e.g., which language to choose for different types of applications).  
     - **Recommendations:** Suggest where Go or Rust might be best suited based on the comparison.

- **research_oriented_query**  
   - Example Query: "Explain the evolution of distributed file systems."  
   - Conclusion Structure:  
     - **Key Insight Summary:** Provide an overview of the major developments in distributed file systems.  
     - **Final Thoughts:** Discuss future directions or potential challenges.  
     - **Implications for Research:** Identify gaps in current research and propose areas for future study.

- **execution_programming_query**  
   - Example Query: "Write a Python script to scrape a website."  
   - Conclusion Structure:  
     - **Key Insight Summary:** Summarize the steps in web scraping and the tools used.  
     - **Final Thoughts:** Mention best practices or common challenges faced in web scraping.  
     - **Recommendations:** Suggest improvements or extensions to the script, like handling dynamic pages or introducing error handling.

- **idea_generation**  
   - Example Query: "Give me startup ideas using blockchain."  
   - Conclusion Structure:  
     - **Key Insight Summary:** Recap the key startup ideas suggested.  
     - **Final Thoughts:** Highlight the feasibility and potential of blockchain-based startups.  
     - **Recommendations:** Provide guidance on pursuing the best startup ideas or exploring new areas.

**Output:** JSON with `footer` object containing `summary`, `final_thoughts`, and `recommendations`.
"""
                ),
                HumanMessagePromptTemplate.from_template(
                    "The query is: {query}, and the report structure is {structure}. The footer summary is: {summary}. The footer thoughts and recommendations are: {final_thoughts}, {recommendations}"
                ),
            ]
        )
        return prompt

    @classmethod
    def get_references_writer_prompt(cls):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
You are a professional report formatter tasked with creating the **references section** for a report based on the section structure and research requirements.

## **Key Requirements for References Framework**
1. **References List:** Create a list of references for the report, citing only those sections where **research=True**.
2. **References Structure:**  
   - For each section requiring research, cite the relevant **sources** used in that section.  
   - **Section Name:** Use the title of the section as the reference category.  
   - **Section ID:** Provide the section ID for clarity.  
   - **Source URL:** Include the URLs or sources from which the research was drawn for that section.
3. **Only Include Research-Based Sections:** Only sections with `research=True` should have references.

## **Example of Reference Structure:**
- Section: *Introduction to Go and Rust*  
  - Research: True  
  - Sources:  
    1. *Source 1*: [Link to academic paper on concurrency models](#)  
    2. *Source 2*: [Rust's concurrency model documentation](#)  

- Section: *Web Scraping with Python*  
  - Research: False  
  - No references needed for this section.

**Output:**  
Provide a list of references in the following format for each researched section:  
  - Section Name: section_name
  - Section ID: section_id
  - Sources:  
    1. *Source Title*: [URL](#)  
    2. *Source Title*: [URL](#)  
"""
                ),
                HumanMessagePromptTemplate.from_template(
                  "The query is: {query}, and the type is: {type_of_query}. The sections are: {sections}"
                ),
            ]
        )
        return prompt
