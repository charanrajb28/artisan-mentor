from pydantic import BaseModel

class GenerateNarrativeRequest(BaseModel):
    prompt: str

class GenerateOpportunityRequest(BaseModel):
    prompt: str

class GenerateScenarioRequest(BaseModel):
    prompt: str