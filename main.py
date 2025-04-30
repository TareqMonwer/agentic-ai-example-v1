import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from third_parties.linkedin import scrape_linkedin_profile

load_dotenv()


LINKEDIN_PROFILE = "https://gist.githubusercontent.com/TareqMonwer/f2bd6927aff7caa6efea1f67481c8641/raw/15d48642c7beab488bef35c61c044c3fde4c741e/profile_1.json"

def main():
    print("Hello from icebreak!")
    openai_key = os.environ.get("OPENAI_API_KEY", "")

    summary_template = """
    Given the Linkedin information {information} about person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = summary_prompt_template | llm

    linkedin_info = scrape_linkedin_profile(LINKEDIN_PROFILE, mock=True)
    
    response = chain.invoke(input={"information": linkedin_info})

    print(response)


if __name__ == "__main__":
    main()
