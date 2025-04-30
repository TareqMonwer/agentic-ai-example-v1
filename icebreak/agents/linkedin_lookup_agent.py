from dotenv import load_dotenv

from icebreak.config.models import LOOKUP_MODEL

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub

from icebreak.tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm =  ChatOpenAI(temperature=0, model=LOOKUP_MODEL)
    
    template = """
    Given the full name {name_of_person} I want you to get it me a link to their LinkedIn profile page.
    Your answer must contain only a URL.
    """
    
    prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)
    
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the LinkedIn page URL"
        )
    ]
    
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(input={"input": prompt_template.format(name_of_person=name)})
    
    profile_url = result.get("output")
    
    if not profile_url:
        raise ValueError("Profile URL wasn't provided in output: ", result)

    return profile_url


if __name__ == "__main__":
     linkedin_url = lookup(name="Eden Marco")
     print(linkedin_url)
