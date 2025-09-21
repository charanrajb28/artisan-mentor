

from fastapi import APIRouter, HTTPException
from ..schemas.insights import Narrative, Opportunity, Scenario
from ..schemas.generate import GenerateNarrativeRequest, GenerateOpportunityRequest, GenerateScenarioRequest
import google.generativeai as genai
import os
from typing import List
import json
from ..services.vector_search import VectorSearchService # New import
from ..schemas.context import Context # New import

router = APIRouter()

# Configure the generative AI client
# IMPORTANT: It is recommended to set the API key as an environment variable for security.
api_key = "AIzaSyB9l2hc3Baf7gXlD2xnCzvbdTsx_ENfllo"
if not api_key:
    raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")

genai.configure(api_key=api_key)

@router.post("/narratives", response_model=List[Narrative])
def generate_narratives(request: GenerateNarrativeRequest):
    """
    Generates audience-targeted narratives based on a free-form prompt.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        # Construct the prompt
        prompt = f"""
        You are an expert storyteller for artisans. Your task is to create compelling narratives.
        A user has the following request: "{request.prompt}"
        Based on this request, generate 3 distinct narratives, each targeted at a different audience segment.
        Ensure each narrative adheres to the following JSON schema:
        {{
            "title": "string",
            "story": "string",
            "audience_segment": "string"
        }}

        Provide the output as a JSON array of Narrative objects.
        """

        response = model.generate_content(prompt)

        # The model can sometimes return markdown formatting, so we need to extract the JSON from the response.
        # Find the start and end of the JSON array.
        json_start = response.text.find('[')
        json_end = response.text.rfind(']') + 1
        json_text = response.text[json_start:json_end]
        
        narratives_data = json.loads(json_text)
        narratives = [Narrative(**data) for data in narratives_data]

        return narratives

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/opportunities", response_model=List[Opportunity])
def generate_opportunities(request: GenerateOpportunityRequest):
    """
    Generates business opportunities for artisans based on a free-form prompt.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        # Construct the prompt
        prompt = f"""
        You are an expert business strategist for artisans. Your task is to propose unconventional channels or use-cases.
        A user has the following request: "{request.prompt}"
        Based on this request, propose 5 unconventional channels or use-cases that align with heritage motifs and current momentum;
        for each, add who-to-contact, entry script, MOQ/packaging guidance, timing window, and evidence chips;
        reject ideas that violate fragility/capacity.

        Output schema:
        {{
            "name": "string",
            "channel_type": "string",
            "why_now": "string",
            "who_to_contact": "string",
            "entry_script": "string",
            "feasibility": "string",
            "packaging": "string",
            "timing_window": "string",
            "evidence": ["string"],
            "sources": ["string"]
        }}

        Provide the output as a JSON array of Opportunity objects.
        """

        response = model.generate_content(prompt)

        # The model can sometimes return markdown formatting, so we need to extract the JSON from the response.
        # Find the start and end of the JSON array.
        json_start = response.text.find('[')
        json_end = response.text.rfind(']') + 1
        json_text = response.text[json_start:json_end]
        
        opportunities_data = json.loads(json_text)
        opportunities = [Opportunity(**data) for data in opportunities_data]

        return opportunities

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scenarios", response_model=List[Scenario])
def generate_scenarios(request: GenerateScenarioRequest):
    """
    Generates scenarios for artisans based on a free-form prompt.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        # Construct the prompt
        prompt = f"""
        You are an expert business strategist for artisans. Your task is to create compelling scenarios.
        A user has the following request: "{request.prompt}"
        Based on this request, generate 3 distinct scenarios.
        Ensure each scenario adheres to the following JSON schema:
        {{
            "title": "string",
            "description": "string",
            "feasibility_status": "string",
            "prep_checklist": ["string"]
        }}

        Provide the output as a JSON array of Scenario objects.
        """

        response = model.generate_content(prompt)

        # The model can sometimes return markdown formatting, so we need to extract the JSON from the response.
        # Find the start and end of the JSON array.
        json_start = response.text.find('[')
        json_end = response.text.rfind(']') + 1
        json_text = response.text[json_start:json_end]
        
        scenarios_data = json.loads(json_text)
        scenarios = [Scenario(**data) for data in scenarios_data]

        return scenarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/opportunities/odd-markets", response_model=List[Opportunity])
def generate_odd_markets(request: GenerateOpportunityRequest):
    """
    Generates odd-market strategies for artisans based on a free-form prompt.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        vector_search_service = VectorSearchService()

        # Retrieve unconventional channels from RAG
        retrieved_contexts = vector_search_service.semantic_retrieve(request.prompt)

        context_data = ""
        if retrieved_contexts:
            context_data = "Here are some unconventional channels/contexts from the knowledge base:\n"
            for context in retrieved_contexts:
                context_data += f"- Content: {context.content}\n  Citation: {context.citation}\n"
            context_data += "\n"

        # Construct the prompt for the generative model
        prompt = f"""
        You are an expert in identifying odd-market strategies for artisans.
        A user has the following request: "{request.prompt}"
        Based on this request and the provided contexts, generate 3 odd-market opportunities.
        For each opportunity, score it by novelty, momentum, and feasibility (e.g., Novelty: 8/10, Momentum: 7/10, Feasibility: 6/10).
        Also, include who-to-contact, entry scripts, and MOQ (Minimum Order Quantity) guidance.

        {context_data}

        Ensure each opportunity adheres to the following JSON schema:
        {{
            "name": "string",
            "channel_type": "string",
            "why_now": "string",
            "who_to_contact": "string",
            "entry_script": "string",
            "feasibility": "string",
            "packaging": "string",
            "timing_window": "string",
            "evidence": ["string"],
            "sources": ["string"],
            "novelty_score": "integer",
            "momentum_score": "integer",
            "feasibility_score": "integer",
            "moq_guidance": "string"
        }}

        Provide the output as a JSON array of Opportunity objects.
        """

        response = model.generate_content(prompt)
        print(response.text) # Print raw response for debugging

        # The model can sometimes return markdown formatting, so we need to extract the JSON from the response.
        # Find the start and end of the JSON array.
        json_start = response.text.find('[')
        json_end = response.text.rfind(']') + 1
        json_text = response.text[json_start:json_end]
        
        opportunities_data = json.loads(json_text)
        opportunities = [Opportunity(**data) for data in opportunities_data]

        return opportunities

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
