from pydantic import BaseModel
from typing import List

class Narrative(BaseModel):
    title: str
    story: str
    audience_segment: str

class Opportunity(BaseModel):
    name: str
    channel_type: str
    why_now: str
    who_to_contact: str
    entry_script: str
    feasibility: str
    packaging: str
    timing_window: str
    evidence: List[str]
    sources: List[str]
    novelty_score: int
    momentum_score: int
    feasibility_score: int
    moq_guidance: str

class Scenario(BaseModel):
    title: str
    description: str
    feasibility_status: str
    prep_checklist: List[str]

class InsightsBundle(BaseModel):
    narratives: List[Narrative]
    opportunities: List[Opportunity]
    scenarios: List[Scenario]

class MentorAdviseRequest(BaseModel):
    prompt: str
    chat_id: int # New field
