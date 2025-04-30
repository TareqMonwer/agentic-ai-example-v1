from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class ProfileSummary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")


profile_summary_parser = PydanticOutputParser(pydantic_object=ProfileSummary)
