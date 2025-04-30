from fastapi import FastAPI
from pydantic import BaseModel

from icebreak.main import linkedin_profile_facts
app = FastAPI()


class ProfileSearch(BaseModel):
    search_query: str
    mock: bool


@app.post("/linkedin-profile-facts/")
def read_item(input: ProfileSearch):
    response = linkedin_profile_facts(input.search_query, input.mock)
    return response
