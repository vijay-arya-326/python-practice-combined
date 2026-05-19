import os
import sys

import requests
import gradio as grd

from dotenv import load_dotenv
from pathlib import Path
from langgraph.graph import START, END
from langgraph.prebuilt import ToolNode, tools_condition
from openai.types.beta.threads.runs import tool_call

from library.validate_env_variables import verify_environment_variables_for_business_discovery_agent
from src.business_discovery.tools.tools_package import toolsList
from src.business_discovery.tools.web_search_tool import web_search_tool
from src.business_discovery.tools.web_search_tool.web_search_tool import searxng_web_search

graph_path = Path.cwd().joinpath("src/business_discovery").joinpath("business_discovery_agent.png")

from dotenv.variables import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph

from library.custom_log import log_errors
from src.business_discovery.agents.llm_agents import chatOllamaLlama, chatOllamaMistral
from src.business_discovery.agents.scope_check_agent import (
    intent_detection,
    business_discovery_agent,
    greeting_node,
    intent_router, handle_out_of_scopeQueries,
)
# from src.business_discovery.agents.scope_check_agent import scope_checker
from src.business_discovery.states.business_discovery_agent_state import BusinessDiscoveryAgentState

env_path = Path.cwd().joinpath("env").joinpath(".env")
print(f"Environment FilePath {env_path}")
load_dotenv(override=True, dotenv_path=env_path)

print("APP_NAME  == ", os.getenv("APP_NAME"))

try:

    graph = StateGraph(BusinessDiscoveryAgentState)
    """ ADDING NODES """
    graph.add_node(business_discovery_agent)
    graph.add_node(intent_detection)
    graph.add_node(handle_out_of_scopeQueries)
    # graph.add_node("tools", ToolNode=toolsList)
    graph.add_node(greeting_node)

    """ CREATING EDGES """
    graph.set_entry_point("intent_detection")
    graph.add_conditional_edges("intent_detection", intent_router)

    # graph.add_conditional_edges("business_discovery_agent", tools_condition, "tools")
    graph.set_finish_point("greeting_node")
    graph.set_finish_point("handle_out_of_scopeQueries")
    graph.set_finish_point("business_discovery_agent")

    gr = graph.compile()
    graph_png = gr.get_graph().draw_mermaid_png()
    with open(graph_path, "wb+") as f:
        f.write(graph_png)


    # -----------------------------
    # Gradio Chat Function
    # -----------------------------
    def chat(message, history):
        """
        message -> current user input
        history -> previous chat history from Gradio
        """
        # Invoke graph
        result = gr.invoke({
            "messages": HumanMessage(content=message),
        })
        # Get last AI message
        ai_response = result["messages"][-1].content

        return ai_response


    # -----------------------------
    # Gradio UI
    # -----------------------------
    demo = grd.ChatInterface(
        fn=chat,
        title="Business Discovery & Business Rules"
    )

    if __name__ == "__main__":
        response  = verify_environment_variables_for_business_discovery_agent()

        if response["error_flag"] == True:
            print("=" * 40)
            print("For missing mandatory environment variables")
            print("="*40)
            for message in response["mandatory_error_list"] + response["optional_error_list"]:
                print(message)

            print("=" *40)

        if response["start_application"] ==  False:
            log_errors("Service not started - reason Mandatory environment variable missing")
            sys.exit(1)

        demo.launch()

except Exception as e:
    print(e)



