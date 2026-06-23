from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import web_search , scrape_url

llm = ChatMistralAI(model = "mistral-small-2506",temperature=0)

# creating the agent 1st - search agent
def build_search_agent():
    return create_agent(
       model= llm,
       tools=[web_search]
    )

#2nd agent reader agent 
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system","you are an expert research writer. you write clear, structured and insightful reports."),
    ("human","""write a detailed research report on the topic: {topic} based on the following research findings: {research}
     structure of the report as :
     - Introduction
     -key findings (min 3 well-explained points)
     -conclusion
     -sources (list all URLs found in the research)
     be detailed factual and professional.
     """)
])
parser = StrOutputParser()

writer_chain = writer_prompt|llm|parser

critic_prompt = ChatPromptTemplate.from_messages([
   ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),])


critic_chain = critic_prompt|llm|parser