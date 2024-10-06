
import os

from langchain_openai import ChatOpenAI
from agent import Agents
from flask import Flask, request, jsonify
from crewai import Crew, Process
from openai import OpenAI
from tasks import TravelTasks
from tools import load_api_key

# Inisialisasi Flask
app = Flask(__name__)

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    try:
        # Ambil data dari request body
        data = request.json
        origin = data.get("origin")
        cities = data.get("cities")
        date_start = data.get("date_start")
        date_end = data.get("date_end")
        interests = data.get("interests")

        # Validasi input
        if not all([origin, cities, date_start, date_end, interests]):
            return jsonify({"error": "All fields are required."}), 400

        # Load API Key dari file atau environment
        api_key = load_api_key()
        if not api_key:
            return jsonify({"error": "API key not found. Please set your API key"}), 500

        # Set API Key untuk OpenAI
       
        openaigpt4 = ChatOpenAI(model='gpt-4o', 
                                     temperature=0.2, 
                                     api_key=api_key)
        # Setup agen dan tugas AI Crew
        agents = Agents()
        tasks = TravelTasks(origin, cities, str(date_start), str(date_end), interests)

        travel_plan = Crew(
            agents=[
                agents.transport_specialist(),
                agents.accomodation_expert(), 
                agents.spot_finder(), 
                agents.expert_travel_agent()
            ],
            tasks=[
                tasks.transport_info(), 
                tasks.accomodation_info(), 
                tasks.gather_city_info(), 
                tasks.plan_itinerary()
            ],
            process=Process.sequential,
            manager_llm=openaigpt4  # Menggunakan OpenAI langsung
        )

        # Proses pembuatan itinerary
        hasil = travel_plan.kickoff()

        # Proses hasil raw dengan ChatGPT
        formatted_result = format_with_chatgpt(hasil.raw)

        # Mengembalikan hasil yang sudah terformat dalam JSON
        return formatted_result
     
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def format_with_chatgpt(raw_data):
    # Template JSON yang digunakan untuk memastikan format yang sesuai
    template_json = {
        "data": {
              "title": "",
              "transportation": [
                   {"type": "", "route": "", "provider_name": "", "departure_time": "", "arrival_time": "", "estimated_cost": "", "note": ""},
              ],
              "acomodation" : [
                  {"hotel_name" : "", "location": "", "estimated_cost": "", "amenities": ""}
              ],
             "itinerary": [
                    {"day": "", "date": "", "activities": [""], "weather": "", "budget":"", "link_image_destination": ""},
              ],       
            "safety_tips": [""],
            "overall_budget_estimate": {
                "range": "",
                "includes": [""]
            }
        }
    }

    # Menyusun permintaan untuk ChatGPT
    prompt = f"""
    Berikut adalah hasil perjalanan dalam format raw:
    {raw_data}

    Tolong format dan pisahkan data ini ke dalam struktur JSON yang **terorganisir dengan sangat jelas dan sesuai dengan template di bawah ini**.
    Pastikan untuk **mematuhi struktur JSON yang diberikan**, mengisi semua bagian yang relevan, dan tidak menambah atau mengurangi elemen apa pun di luar dari template.
    
    **Template JSON**:

    {template_json}

    Harap output dalam format JSON persis seperti template di atas, dan isi semua data yang relevan dari informasi perjalanan yang disediakan.
    Jangan ubah format atau struktur JSON. Pastikan hasil JSON memiliki semua key seperti dalam template di atas, baik yang kosong maupun yang terisi data.
    """

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    # Mengirim permintaan ke ChatGPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Mengambil dan mengembalikan hasil dari ChatGPT
    return response.choices[0].message.content



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001)
