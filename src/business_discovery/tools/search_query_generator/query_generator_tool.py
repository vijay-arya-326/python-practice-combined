from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel
import copy

from src.business_discovery.agents.llm_agents import chatOllamaMistral, chatOllamaGemma
from src.business_discovery.prompts.search_query_genarator import search_query_prompt


class search_query_response_format(BaseModel):
    search_query: list[str]


@tool
def search_engine_query_generator(user_query:str):
    """
    Generate search engine query for business discovery
    :param user_query:
    :return:
    """
    system_prompt  = SystemMessage(content=search_query_prompt)

    human_message = HumanMessage(content=f"""{user_query}""")

    messages = [system_prompt, human_message]
    llm_agent = chatOllamaMistral().with_structured_output(search_query_response_format)
    res = llm_agent.invoke(messages)
    return res.search_query


if __name__ == "__main__":
    res = search_engine_query_generator.invoke({"user_query":"user onboarding for saving account east west bank, Philippines"})
    print(res)