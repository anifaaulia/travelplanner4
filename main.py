import os
from dotenv import load_dotenv 
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage

#variabel lingkungan dari file .env
load_dotenv()

#mengambil API key dari variabel lingkungan
api_key = os.getenv('OPENAI_API_KEY')

# Inisialisasi ChatOpenAI dengan API key dan parameter lainnya
openaigpt4 = ChatOpenAI(model='gpt-4', 
                        temperature=0.2, 
                        api_key=api_key)

class AICrewMember:
    def __init__(self, name, role, task_prompt):
        self.name = name
        self.role = role
        self.task_prompt = task_prompt

    def perform_task(self, data):
        # Format the prompt with the provided data
        formatted_prompt = self.task_prompt.format(**data)
        
        # Prepare the message in the expected format
        messages = [HumanMessage(content=formatted_prompt)]
        
        # Get the response from the GPT-4 model
        response = openaigpt4(messages)
        
        return response.content.strip()

def main():
    st.title("AI Travel Planner")

    # Mengajukan pertanyaan kepada pengguna
    origin = st.text_input("From where will you be traveling from?")
    cities = st.text_input("What are the cities options you are interested in visiting? (separate by commas)")
    date_range = st.text_input("What is the date range you are interested in traveling?")
    interests = st.text_input("What are some of your high level interests and hobbies?")

    if st.button("Generate Itinerary"):
        # Data yang akan diproses oleh AI Crew
        data = {
            "origin": origin,
            "cities": cities,
            "date_range": date_range,
            "interests": interests
        }

        # Definisikan AI Crew
        ai_crew = [
            AICrewMember(
                name="Transport Specialist",
                role="transportation",
                task_prompt="You are a travel agent specializing in transportation. Based on the following information, recommend the best transportation options for traveling from {origin} to {cities} between {date_range}."
            ),
            AICrewMember(
                name="Accommodation Expert",
                role="accommodation",
                task_prompt="You are an expert in travel accommodations. Based on the following information, recommend the best places to stay in {cities} during the date range of {date_range} considering interests in {interests}."
            ),
            AICrewMember(
                name="Activity Planner",
                role="activities",
                task_prompt="You are an activity planner. Based on the following information, suggest the top activities and experiences to enjoy in {cities} given the date range {date_range} and interests in {interests}."
            )
        ]

        # Mengumpulkan hasil dari masing-masing AI Crew
        results = {}
        for member in ai_crew:
            result = member.perform_task(data)
            results[member.role] = result
            st.write(f"**{member.name} ({member.role}):**\n{result}")

        # Menggabungkan hasil menjadi itinerary
        itinerary = f"""
        **Travel Itinerary:**
        
        - **Transportation:** {results.get('transportation', 'No data')}
        - **Accommodation:** {results.get('accommodation', 'No data')}
        - **Activities:** {results.get('activities', 'No data')}
        """

        st.markdown(itinerary)

if __name__ == "__main__":
    main()
