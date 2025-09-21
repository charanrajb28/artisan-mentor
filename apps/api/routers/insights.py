from fastapi import APIRouter, HTTPException
from ..schemas.insights import InsightsBundle, Narrative, Opportunity, Scenario
import requests
import json
from ..services.google_trends_service import GoogleTrendsService
from ..services.web_search_service import WebSearchService
from ..services.vector_search import VectorSearchService # New import
from ..services.signals import SignalsService # New import

router = APIRouter()

google_trends_service = GoogleTrendsService()
web_search_service = WebSearchService()
vector_search_service = VectorSearchService() # Instantiate
signals_service = SignalsService() # Instantiate

@router.get("/{profile_id}", response_model=InsightsBundle)
def get_insights(profile_id: str):
    try:
        # Derive a general prompt from profile_id
        general_prompt = f"insights for artisan profile {profile_id}"

        # 1. Retrieve (Vector Search)
        retrieved_contexts = vector_search_service.semantic_retrieve(general_prompt)
        context_data = ""
        if retrieved_contexts:
            context_data = "Here is some relevant context from the knowledge base:\n"
            for context in retrieved_contexts:
                context_data += f"- Content: {context.content}\n  Citation: {context.citation}\n"
            context_data += "\n"

        # 2. Signals (Dummy for now, will be derived from profile/trends/web search)
        craft_profile = {"name": f"Artisan {profile_id}"}
        # For signals, we can use Google Trends data as an example
        trend_data = google_trends_service.get_trend_data_for_keyword(general_prompt)
        signals = {
            "momentum_4w": trend_data['average_score'], # Using average score as momentum
            "days_to_event": 16, # Dummy
            "event_name": "Local Craft Fair" # Dummy
        }
        evidence_chips = signals_service.get_evidence_chips(craft_profile, signals)


        # 3. Generate
        # Narratives
        narrative_prompt = f"Generate narratives for artisan {profile_id} based on: {general_prompt}. Context: {context_data}"
        narrative_response = requests.post(
            "http://localhost:8000/generate/narratives",
            json={"prompt": narrative_prompt}
        )
        narrative_response.raise_for_status() # Correctly indented
        narratives_data = narrative_response.json()
        narratives = [Narrative(**data) for data in narratives_data]

        # Opportunities
        opportunity_prompt = f"Generate opportunities for artisan {profile_id} based on: {general_prompt}. Context: {context_data}. Signals: {evidence_chips}"
        opportunity_request_payload = {"prompt": opportunity_prompt}
        opportunity_response = requests.post(
            "http://localhost:8000/generate/opportunities",
            json=opportunity_request_payload
        )
        opportunity_response.raise_for_status() # Correctly indented
        opportunities_data = opportunity_response.json()
        opportunities = [Opportunity(**data) for data in opportunities_data]
        # Add evidence chips to opportunities (already done in mentor.py, but for BFF, we might want to do it here)
        # For now, assuming generate/opportunities returns opportunities with evidence chips

        # Scenarios
        scenario_prompt = f"Generate scenarios for artisan {profile_id} based on: {general_prompt}. Context: {context_data}"
        scenario_request_payload = {"prompt": scenario_prompt}
        scenario_response = requests.post(
            "http://localhost:8000/generate/scenarios",
            json=scenario_request_payload
        )
        scenario_response.raise_for_status() # Correctly indented
        scenarios_data = scenario_response.json()
        scenarios = [Scenario(**data) for data in scenarios_data]

        # 4. Compose
        return InsightsBundle(
            narratives=narratives,
            opportunities=opportunities,
            scenarios=scenarios
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with generation service: {e}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from generation service.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))