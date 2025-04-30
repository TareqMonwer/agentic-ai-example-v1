from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from icebreak.agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from icebreak.config.models import SUMMARY_MODEL
from icebreak.third_parties.linkedin import scrape_linkedin_profile

load_dotenv()


LINKEDIN_PROFILE = "https://gist.githubusercontent.com/TareqMonwer/f2bd6927aff7caa6efea1f67481c8641/raw/15d48642c7beab488bef35c61c044c3fde4c741e/profile_1.json"

def linkedin_profile_facts(profile_name_query: str, mock: bool):
    summary_template = """
    Given the Linkedin information {information} about person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(temperature=0, model=SUMMARY_MODEL)

    chain = summary_prompt_template | llm

    if mock:
        linkedin_info = scrape_linkedin_profile(LINKEDIN_PROFILE, mock=True)
    else:
        linkedin_url = linkedin_lookup_agent(profile_name_query)
        linkedin_info = scrape_linkedin_profile(linkedin_url)
    
    response = chain.invoke(input={"information": linkedin_info})

    print(response)


if __name__ == "__main__":
    linkedin_profile_facts("Akshay Saini Linkedin Profile", False)
