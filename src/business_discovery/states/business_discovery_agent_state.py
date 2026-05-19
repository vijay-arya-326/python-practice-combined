from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages


class BusinessDiscoveryAgentState(TypedDict):
    messages: Annotated[List[str], add_messages]
    intent:str = "GREETING"
    reason_for_out_of_scope:str
    web_search_queries: list[str]

class IntentDetectionStructure(TypedDict):
    intent:str
    reason_for_out_of_scope:str