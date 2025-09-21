from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session # New import
from ..schemas.insights import MentorAdviseRequest
import requests
import json
import google.generativeai as genai
from ..services.google_trends_service import GoogleTrendsService
from ..services.web_search_service import WebSearchService
from ..services.vector_search import VectorSearchService
import traceback
from .auth import get_current_user # New import
from ..database import User as DBUser, SessionLocal, ChatSession as DBChatSession # New imports

router = APIRouter()

# Dependency to get DB session (copied from chat.py)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/advise")
async def mentor_advise(request: MentorAdviseRequest, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Provides mentor-mode advisory based on a natural language prompt.
    """
    try:
        # Load chat session and state
        chat_session = db.query(DBChatSession).filter(DBChatSession.id == request.chat_id, DBChatSession.owner_id == current_user.id).first()
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        conversation_state = chat_session.state # Get current state
        
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt_lower = request.prompt.lower()
        response_text = ""
        handled = False

        if "narrative" in prompt_lower:
            handled = True
            narrative_request_payload = {"prompt": request.prompt}
            narrative_response = requests.post(
                "http://localhost:8000/generate/narratives",
                json=narrative_request_payload
            )
            narrative_response.raise_for_status()
            narratives_data = narrative_response.json()

            response_text += "### Narratives\n"
            for narrative in narratives_data:
                response_text += (
                    f"- **Title:** {narrative['title']}\n"
                    f"  **Story:** {narrative['story']}\n"
                    f"  **Audience:** {narrative['audience_segment']}\n\n"
                )

        if "opportunity" in prompt_lower:
            handled = True
            opportunity_request_payload = {"prompt": request.prompt}
            opportunity_response = requests.post(
                "http://localhost:8000/generate/opportunities",
                json=opportunity_request_payload
            )
            opportunity_response.raise_for_status()
            opportunities_data = opportunity_response.json()

            response_text += "### Opportunities\n"
            for opp in opportunities_data:
                response_text += (
                    f"- **Name:** {opp['name']}\n"
                    f"  **Channel:** {opp['channel_type']}\n"
                    f"  **Why Now:** {opp['why_now']}\n\n"
                )

        if "scenario" in prompt_lower:
            handled = True
            scenario_request_payload = {"prompt": request.prompt}
            scenario_response = requests.post(
                "http://localhost:8000/generate/scenarios",
                json=scenario_request_payload
            )
            scenario_response.raise_for_status()
            scenarios_data = scenario_response.json()

            response_text += "### Scenarios\n"
            for scenario in scenarios_data:
                response_text += (
                    f"- **Title:** {scenario['title']}\n"
                    f"  **Description:** {scenario['description']}\n"
                    f"  **Feasibility:** {scenario['feasibility_status']}\n\n"
                )

        if not handled:
            # Extract keyword for Google Trends
            keyword_extraction_prompt = f"""
            From the following user request, extract the most relevant 2-3 word keyword for a Google Trends search.
            Your output should ONLY be the keyword, with no additional text, explanations, or punctuation.
            User request: "{request.prompt}"
            Keyword:
            """
            keyword_response = model.generate_content(keyword_extraction_prompt)
            keyword = keyword_response.text.strip()
            if not keyword: # Fallback if model doesn't return a keyword
                keyword = " ".join(request.prompt.split()[:3]) # Use first 3 words as fallback

            # Google Trends
            trends_service = GoogleTrendsService()
            trend_data = trends_service.get_trend_data_for_keyword(keyword) # New call

            trends_data_str = f"Google Trends data for '{trend_data['keyword']}':\n"
            trends_data_str += f"- Average interest score: {trend_data['average_score']}\n"
            trends_data_str += f"- Top 3 related queries: {', '.join(trend_data['related_queries'])}\n\n"

            # Web Search for festivals
            web_search_service = WebSearchService()
            search_query = f"upcoming festivals and events for {request.prompt}"
            search_results = web_search_service.search(search_query)
            
            search_data = f"Here are some upcoming festivals and events related to '{request.prompt}':\n"
            if search_results:
                for result in search_results:
                    search_data += f"- {result['title']}: {result['href']}\n"
            else:
                search_data += "No upcoming festivals or events found.\n"
            search_data += "\n"

            # Vector Search for relevant contexts
            vector_search_service = VectorSearchService()
            retrieved_contexts = vector_search_service.semantic_retrieve(request.prompt)

            context_data = "Here is some relevant context from the knowledge base:\n"
            if retrieved_contexts:
                for context in retrieved_contexts:
                    context_data += f"- Content: {context.content}\n  Citation: {context.citation}\n"
            else:
                context_data += "No relevant context found.\n"
            context_data += "\n"

            prompt_for_model = (
                f"As an Artisan Mentor, provide a concise and helpful advisory "
                f"based on the user's request: \"{request.prompt}\"\n\n"
                f"Current conversation state: {conversation_state}\n\n" # Pass state to model
                f"Here is some additional context from Google Trends:\n{trends_data_str}"
                f"Here is some additional context from a web search for upcoming festivals and events:\n{search_data}"
                f"Here is some additional context from the knowledge base:\n{context_data}"
            )
            model_response = model.generate_content(prompt_for_model)
            response_text = trends_data_str + search_data + context_data + model_response.text

        # Update conversation state (placeholder for actual state management logic)
        # For now, just store the last prompt and response
        chat_session.state = {"last_prompt": request.prompt, "last_response": response_text}
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

        return {"response": response_text}

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with generation service: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error communicating with generation service: {e}")
    except json.JSONDecodeError:
        print("Invalid JSON response from generation service.")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Invalid JSON response from generation service.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))