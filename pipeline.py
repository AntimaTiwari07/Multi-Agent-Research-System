# agents call |writer_chain|critic_chain|final output
from agents import build_reader_agent, build_search_agent,critic_chain,writer_chain
from langchain.messages import HumanMessage
from rich import print

def run_research_pipeline(topic:str)->dict:
    state = {}

    #search agent working
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
         "messages": [
        {
            "role": "user",
            "content": f"Find recent,reliable and detailed information about {topic}"
        }
    ]
    })
    state["search_result"] = search_result['messages'][-1].content
    print("\n search agent result = ",search_result)

    print("\n 2nd agent is working................")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [
        HumanMessage(
            content=f"Based on the following result about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"search results:\n{state['search_result'][:800]}"
        )
    ]
    })
    state['scraped_content'] = reader_result['messages'][-1].content
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']} "
    )
    state["report"] = writer_chain.invoke({"topic":topic,"research":research_combined})
    print("\n\n\n\n")
    print(state["report"])
    state["feedback"] = critic_chain.invoke({"report":state["report"]})

    print("\n critic report \n",state["feedback"])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research Topic : ")
    run_research_pipeline(topic)


