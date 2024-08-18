from langchain.chat_models import ChatOpenAI
from tasks import AICrewMember

def initialize_ai_model(api_key):
    return ChatOpenAI(
        model='gpt-4', 
        temperature=0.2, 
        api_key=api_key
    )

def create_ai_crew(openaigpt4):
    return [
        AICrewMember(
            name="Transport Specialist",
            role="transportation",
            task_prompt="You are a travel agent specializing in transportation. Based on the following information, recommend the best transportation options for traveling from {origin} to {cities} between {date_range}.",
            openaigpt4=openaigpt4
        ),
        AICrewMember(
            name="Accommodation Expert",
            role="accommodation",
            task_prompt="You are an expert in travel accommodations. Based on the following information, recommend the best places to stay in {cities} during the date range of {date_range} considering interests in {interests}.",
            openaigpt4=openaigpt4
        ),
        AICrewMember(
            name="Activity Planner",
            role="activities",
            task_prompt="You are an activity planner. Based on the following information, suggest the top activities and experiences to enjoy in {cities} given the date range {date_range} and interests in {interests}.",
            openaigpt4=openaigpt4
        )
    ]

def generate_itinerary(data, ai_crew):
    results = {}
    for member in ai_crew:
        result = member.perform_task(data)
        results[member.role] = result
    
    itinerary = f"""
    **Travel Itinerary:**
    
    - **Transportation:** {results.get('transportation', 'No data')}
    - **Accommodation:** {results.get('accommodation', 'No data')}
    - **Activities:** {results.get('activities', 'No data')}
    """
    
    return itinerary
