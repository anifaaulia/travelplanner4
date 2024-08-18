import streamlit as st
from agent import initialize_ai_model, create_ai_crew, generate_itinerary
from tools import load_api_key


def main():
    st.title("AI Travel Planner")

    # Mengajukan pertanyaan kepada pengguna
    origin = st.text_input("From where will you be traveling from?")
    cities = st.text_input("What are the cities options you are interested in visiting? (separate by commas)")
    date_range = st.text_input("What is the date range you are interested in traveling?")
    interests = st.text_input("What are some of your high level interests and hobbies?")

    if st.button("Generate Itinerary"):
        #Load API key from environtment
        api_key = load_api_key()
        if not api_key:
            st.error("API key not found. Please set your API")
            return
        #Initialize AI model 
        openaigpt4 = initialize_ai_model(api_key)

        # Data yang akan diproses oleh AI Crew
        data = {
            "origin": origin,
            "cities": cities,
            "date_range": date_range,
            "interests": interests
        }


        # Create AI Crew
        ai_crew = create_ai_crew(openaigpt4)

        #Generate Itinerary
        itinerary = generate_itinerary(data, ai_crew)

        #Display Itinerary
        st.markdown(itinerary)
        
if __name__ == "__main__":
    main()
