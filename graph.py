from typing import List, Sequence
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain, tools
from langgraph.prebuilt import ToolNode
from typing import Annotated,Sequence, Literal, TypedDict



REFLECT = "reflect"
TOOL = "tool"
GENERATE = "generate"
graph = MessageGraph()

def generate_node(state):
    response = generation_chain.invoke({
        "messages": state
    })
    if not isinstance(response, BaseMessage):
        return AIMessage(content=str(response))
    return response


def reflect_node(messages):
    response = reflection_chain.invoke({
        "messages": messages
    })
    content = response.content if isinstance(response, BaseMessage) else str(response)
    return [HumanMessage(content=content)]

tool_node = ToolNode(tools)





graph.add_node(GENERATE, generate_node)
#graph.add_node(REFLECT, reflect_node)
graph.add_node(TOOL, tool_node)
graph.set_entry_point(GENERATE)


def should_check(messages):
    last_message = messages[-1]
    if last_message.tool_calls:
        return TOOL
    return END


# def should_continue(state):
#     if (len(state) > 6):
#         return END
#     return REFLECT


graph.add_conditional_edges(GENERATE, should_check)
graph.add_edge(TOOL, GENERATE)
#graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()


response = app.invoke(HumanMessage(content="filter working items"))

print(response)