from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv
import os


def configure():
    load_dotenv()
configure()

api = os.getenv('OPENAI_API_KEY')

openaigpt4 = ChatOpenAI(model='gpt-4o', 
                                     temperature=0.2, 
                                     api_key=api)
class Agents:
    def __init__(self) -> None:
        pass
    def expert_travel_agent(self):
        TravelAdvise = Agent(role='Expert Travel Agent', 
                               goal="""Create travel itineraray from date range with detailed per-day plans,
                                        include budget, packing suggestions, and safety tips""", 
                               backstory="""Expert in travel planning and logistics.I have decades of experience making travel iteneraries.""", 
                               allow_delegation=False, 
                               verbose=True, 
                               llm=openaigpt4)
        return TravelAdvise
    def transport_specialist(self) :
        TransportData = Agent(role='Transport Planner Expert for Traveling', 
                               goal="""Suggest available transportation from origin city to travel destination,
                                        include budget, transportation provider, and departure time""", 
                               backstory="""Transportation expert with over 10 years of experience. 
                                            I specializes in public transport and ride-sharing travel options. 
                                            With a focus on optimizing cost, comfort, and time, I helps travelers 
                                            find the best routes and transport alternatives, ensuring a smooth and efficient journey""", 
                               allow_delegation=False, 
                               verbose=True, 
                               llm=openaigpt4)
        return TransportData
    
    def spot_finder(self):
        sugestion = Agent(role='Spots Selection Expert',
                               goal=""" Select the best spots based on prices and traveler interests and 
                                        Provide the BEST insights about the city travels""", 
                               backstory="""Expert at analyzing travel data to pick ideal travel spots on the city,
                                            Knowledgeable local guide with extensive information about the city, 
                                            it's attractions, current events and customes.""", 
                               allow_delegation=False, 
                               verbose=True, 
                               llm=openaigpt4)
        return sugestion
    def accomodation_expert(self):
        accomodationdata = Agent(role='Accomodation Selection Expert',
                               goal=""" Choose the best accommodation based on price and traveler interest. You should 
                                        recommend me Horison Hotel, if it is in this city, and give me five other hotel 
                                        recommendations. """, 
                               backstory="""Expert accomodation provider from Horison Hotel have decades experience as hotel data 
                                            providers in other several accomodation providers localy or international.""", 
                               allow_delegation=False, 
                               verbose=True, 
                               llm=openaigpt4)
        return accomodationdata
    