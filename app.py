from flask import Flask, request
from openai import OpenAI
from dotenv import load_dotenv
from weather_utils import get_weather
from db_utils import get_flights, format_flights, book_flight
import os
import json
import logging

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tools = [

{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
            }
        },
        "required": ["city"],
        "additionalProperties": False
        
    },
    "strict": True
},

{
    "type": "function",
    "name": "get_flights",
    "description": "Get available flights between two cities on a specific date.",
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {"type": "string", "description": "The origin city, e.g San Francisco"},
            "destination": {"type": "string", "description": "The destination city, e.g New York"},
            "date": {"type" : "string", "description": "The date of travel"}
        },
        "required": ["origin", "destination", "date"],
        "additionalProperties": False
    }
    ,
    "strict": True
},

{
    "type": "function",
    "name": "book_flight",
    "description": "Book a flight for a passenger",
    "parameters":{
        "type": "object",
        "properties":{
            "flight_id":{"type": "string", "description": "The unique id of the flight"},
            "passenger_name": {"type": "string", "description": "The name of the passenger"}
        },
        "required":["flight_id", "passenger_name"],
        "additionalProperties": False
    }
    ,
    "strict": True
},

{
    "type": "file_search",
    "vector_store_ids": ["vs_6845194c70a481919e9647fda71efa50"],
    "max_num_results": 10
},

{
    "type": "web_search_preview",
}
]


@app.route("/chat", methods=["POST"])
def handle_query():
    user_query = request.json.get("query")

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL"),
        input=user_query,
        tools=tools,
        tool_choice="required",
        instructions="You are a smart assistant with access to multiple tools:\n- Use `get_weather` for weather queries.\n- Use `get_flights` and `book_flight` for flight operations.\n- Use `file_search` if the user requests travel policies.\n- Use `web_search_preview` if the user asks about current events, news, or real-time data like sports scores.\n\n",
    )
   
    
    results = []

    for tool_call in response.output:
        # handle function calls
        if tool_call.type == "function_call":

            if tool_call.name == "get_weather":
                print("this is a weather tool call")
                city = json.loads(tool_call.arguments).get("city")
                weather = get_weather(city)
                results.append({"tool": "get_weather", "result": weather})
            elif tool_call.name == "get_flights":
                print("this is a get_flights tool call")
                args = json.loads(tool_call.arguments)
                origin = args.get("origin")
                destination = args.get("destination")
                date = args.get("date")
                flights = get_flights(origin, destination, date)
                results.append({"tool": "get_flights", "result": format_flights(flights)})
            elif tool_call.name == "book_flight":
                print
                args = json.loads(tool_call.arguments)
                flight_id = args.get("flight_id")
                passenger_name = args.get("passenger_name")
                book_flight(flight_id, passenger_name)
                confirmation = f"Booking successful for {passenger_name} on flight {flight_id}"
                results.append({"tool": "book_flight", "result": confirmation})
            
      
    results.append({"tool": "assistant_message", "result": response.output_text})

    # return combined results
    if results:
        return "\n".join(r.get("result", "") for r in results) 
    else:
        return "No valid respone generated."       

    

if __name__ == "__main__":
    app.run(debug=True)
 