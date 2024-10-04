import streamlit as st
from agent import *
from tasks import *
from tools import load_api_key
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(
    api_key=os.environ['OPENAI_API_KEY'],  
)

def main():
    st.title("GEMA AI Travel Planner")

    # Mengajukan pertanyaan kepada pengguna
    origin = st.text_input("From where will you be traveling from?")
    cities = st.text_input("What are the cities options you are interested in visiting? (separate by commas)")

    # Create two columns for date start and date end
    col1, col2 = st.columns(2)

    with col1:
        date_start = str(st.date_input("Date Start", value=None))

    with col2:
        date_end = str(st.date_input("Date End", value=None))
        
    interests = st.text_input("What are some of your high level interests and hobbies?")

    if st.button("Generate Itinerary"):
        # Load API key from environment
        api_key = load_api_key()
        if not api_key:
            st.error("API key not found. Please set your API")
            return
        
        # Initialize AI model 
        # openaigpt4 = initialize_ai_model(api_key)

        # Data yang akan diproses oleh AI Crew
        openaigpt4 = ChatOpenAI(model='gpt-4o', 
                                     temperature=0.2, 
                                     api_key=api)
          
        agents = Agents()
        tasks = TravelTasks(origin,
                            cities,
                            str(date_start), 
                            str(date_end),
                            interests)


        travel_plan = Crew(
            agents=[agents.transport_specialist(), agents.accomodation_expert(), agents.spot_finder(), agents.expert_travel_agent()],  # Daftar agen
            tasks=[tasks.transport_info(), tasks.accomodation_info(), tasks.gather_city_info(), tasks.plan_itinerary()],  # Daftar tugas
            process=Process.sequential,  # Pilih process (sequential atau parallel)
            manager_llm=openaigpt4  # Model LLM (gpt-4) 
        )

        # Menampilkan hasil saran dari AI agents
        st.write("Model is processing the answer, please wait...")
        hasil = travel_plan.kickoff()
        # st.success("Itinerary:")
        # st.markdown(hasil)
        print(travel_plan)
        # # # # Create AI Crew
        # # ai_crew = create_ai_crew(openaigpt4)

        # # # #Generate Itinerary
        # itinerary = generate_itinerary(data, Crew)

        # # Display Itinerary
        # st.markdown(itinerary)
        
if __name__ == "__main__":
    main()
