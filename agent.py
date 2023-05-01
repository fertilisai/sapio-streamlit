from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
# from gradio_tools import StableDiffusionTool

# tool_list = ["serpapi", "llm-math", "requests_all", "wikipedia", "python_repl", "terminal", "human"]


def ask_agent(message, tool_list, ddg=False, stableDiffusion=False):

    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     temperature=0,
                     # max_tokens=150,
                     top_p=1,
                     frequency_penalty=0,
                     presence_penalty=0
                     )
    tools = load_tools(tool_list, llm=llm)

    if ddg:
        tools.append(DuckDuckGoSearchRun())

    # if stableDiffusion:
    #     tools.append(StableDiffusionTool().langchain)

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False, return_intermediate_steps=True)

    # return agent.run(message)
    return agent({"input": message})
