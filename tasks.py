from crewai import Task
from agent import *
from tools import *
class TravelTasks:
    def __init__(self, origin, city, date_start, date_end, interests) :
        self.origin = origin
        self.city = city 
        self.date_start = date_start 
        self.date_end = date_end 
        self.interests = interests 


    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def plan_itinerary(self):
        plan = Task(
            description=
                f"""
            **Task1**: Give list of detailded information about tranportation that can be taken from {self.origin} to {self.city} with estimated costs and departure time
            **Task2**: Develop Comprehensif Travel Itinerary from {self.date_start} to {self.date_end} 
            **Description**: Expand the city guide into a per-day travel itinerary with detailed 
                per-day plans, including weather forecasts, places to eat, packing suggestions, 
                and a budget breakdown. You MUST suggest actual places to visit, 
                If available use  Hotel at {self.city} to stay else use provided accomodation,
                and actual restaurants to go to. This itinerary should cover all aspects of the trip, 
                from arrival to departure, integrating the city guide information with practical travel logistics.

            **Parameters**: 
            - Origin: {self.origin}
            - City: {self.city}
            - Date Range: {self.date_start} to {self.date_end}
            - Traveler Interests: {self.interests}

            **Note**: {self.__tip_section()}
        """
            ,
            agent=Agents().expert_travel_agent(),
            expected_output=(
                """ Comprehensif detailed information list about the city for developing travel plan iteneraries"""
            )
        )
        return plan
    

    def gather_city_info(self):
        return Task(
            description=
                f"""
                    **Task**:  Gather In-depth City Guide Information
                    **Description**: Compile an in-depth guide for the selected city, gathering information about 
                        key attractions, local customs, special events, and daily activity recommendations. 
                        This guide should provide a thorough overview of what the city has to offer, including 
                        hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high-level costs.

                    **Parameters**: 
                    - Origin: {self.origin}
                    - Cities: {self.city}
                    - Interests: {self.interests}
                    - Date Range: {self.date_start} to {self.date_end} 

                    **Note**: {self.__tip_section()}
                """,
            tools=[tavily_tool],
            agent=Agents().spot_finder(),
            expected_output=(
                """ Comprehensif detailed information list about the city for developing travel plan iteneraries"""
            )
        )
    
    def accomodation_info(self):
        return Task(
        description=
            f"""
                **Task**: Gather In-depth City Accommodation Information
                **Description**: First, search for 3 Hotel in {self.city}. If   Hotel is found, gather 
                    its address, estimated price, and amenities. Explain detail location. recomend me from cheap to expensive price.

                **Parameters**: 
                - Origin: {self.origin}
                - Cities: {self.city}
                - Interests: {self.interests}
                - Date Range: {self.date_start} to {self.date_end}

                **Note**: {self.__tip_section()}
            """
        ,
        agent=Agents().accomodation_expert(),
        expected_output=(
            """
            output -> Must return   Hotel details (location, price, amenities) if available. 
            If   Hotel is not available, search for another hotel and return its details (location, price, amenities).
            task -> Search   Hotel in the city.
            """
        ),
        tools=[tavily_tool],
    )
    
    def transport_info(self):
        return Task(
            description=
                f"""
                    **Task**:  Gather In-depth Transportation Information
                    **Description**: Compile selected tarnsportation that must used from {self.origin} to {self.city}, 
                        should gathering information on {self.date_start} about provider name, estimasted price, and departure time.  

                    **Parameters**: 
                    - Origin: {self.origin}
                    - Cities: {self.city}
                    - Interests: {self.interests}
                    - Date Range: {self.date_start} to {self.date_end} 

                    **Note**: {self.__tip_section()}
        """
            ,
            agent=Agents().transport_specialist(),
            expected_output=(
            #output -> provider name, price, time                
                f""" Comprehensif detailed information about the provider name, estimasted price, and departure time from {self.origin} to {self.city}"""
            ),
            tools=[tavily_tool],
        )