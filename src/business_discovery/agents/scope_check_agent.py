import sys
from typing import Literal

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END
from src.business_discovery.agents.llm_agents import chatOllamaMistral, chatOllamaLlama, chatOllamaGemma4
from src.business_discovery.states.business_discovery_agent_state import BusinessDiscoveryAgentState, \
    IntentDetectionStructure
from src.business_discovery.tools.tools_package import toolsList


def intent_detection(state: BusinessDiscoveryAgentState) -> BusinessDiscoveryAgentState:
    _SCOPE_CHECK_SYSTEM = """
    You are a query classifier for "Business Discovery Process", assistant.
    Classify the user's message into exactly one of these three categories:
    IN_SCOPE — IN_SCOPE — User wants to understand, analyze, design, or extract information related to Business Discovery, including business processes, onboarding journeys, eligibility, KYC/AML, APIs, workflows, operational requirements, compliance, documentation, and BRs (Business Rules).
    GREETING — The message is a greeting, introduction, or casual small talk (e.g., "Hi", "Hello", "How are you?", "Good morning", "What can you do?").
    OUT_OF_SCOPE — Any topic unrelated to business discovery.
    STRICTLY Reply with ONLY one word: IN_SCOPE, GREETING, or OUT_OF_SCOPE.
    """

    # user_message = HumanMessage(content=state["messages"])
    system_message = SystemMessage(content=_SCOPE_CHECK_SYSTEM)

    # print(system_message)
    # print(user_message)
    messages = [system_message] + state["messages"]
    response =  chatOllamaMistral().with_structured_output(IntentDetectionStructure).invoke(messages)

    state["intent"] = response["intent"].strip().upper()
    state["reason_for_out_of_scope"] = response["reason_for_out_of_scope"]
    print(state)
    return state




def business_discovery_agent(state:BusinessDiscoveryAgentState) -> BusinessDiscoveryAgentState:
    print("=" * 15)
    print(" Inside Business Discovery Agent")
    print("=" * 15)
    llm = chatOllamaGemma4() #.bind_tools(toolsList)
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return state


def intent_router(state: BusinessDiscoveryAgentState)->Literal[
"business_discovery_agent", "greeting_node", "handle_out_of_scopeQueries"
]:
    print("-" * 15)
    print(f"Inside Detected Intent")
    print("-" * 15)
    user_intent = state["intent"]
    if user_intent == "OUT_OF_SCOPE":
        return "handle_out_of_scopeQueries"
    elif user_intent == "IN_SCOPE":
        return "business_discovery_agent"
    elif user_intent == "GREETING":
        return "greeting_node"


def greeting_node(state: BusinessDiscoveryAgentState):
    print("="*15)
    print("Inside Greeting Node")
    print("=" * 15)
    sys_message = SystemMessage(content="""
           Introduce yourself with your capabilities related to business discovery in 100 to 150 words.
       """)
    messages = [sys_message] + state["messages"]
    response = chatOllamaMistral().invoke(messages)
    state["messages"].append(response.content)
    return state


def handle_out_of_scopeQueries(state: BusinessDiscoveryAgentState):
    print("=" * 15)
    print("Inside Out Of ScopeQueries")
    print("=" * 15)
    sys_message = SystemMessage(content="""
        Mention about query not related to you.
        Introduce yourself with your capabilities related to business discovery in 200 to 300 words.
    """)
    messages = [sys_message] + state["messages"]
    response = chatOllamaMistral().invoke(messages)
    state["messages"].append(response.content)
    return state