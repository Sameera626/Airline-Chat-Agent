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
        input=[
            {
                "role": "system",
                "content": (
                    "You are a smart assistant with access to multiple tools:\n"
                    "- Use `get_weather` for weather queries.\n"
                    "- Use `get_flights` and `book_flight` for flight operations.\n"
                    "- Use `file_search` if the user requests information from documents.\n"
                    "- Use `web_search_preview` if the user asks about current events, news, or real-time data like sports scores.\n\n"
                    "Use the most appropriate tool and return the result."
                )
            },
            {"role": "user", "content": user_query}
    ],
        tools=tools,
        tool_choice="auto"
    )
   
    
    results = []
    for tool_call in response.output:
        # handle function calls
        if tool_call.type == "function_call":

            if tool_call.name == "get_weather":
                city = json.loads(tool_call.arguments).get("city")        
                weather = get_weather(city)
                results.append({"tool": "get_weather", "result": weather})
            elif tool_call.name == "get_flights":
                args = json.loads(tool_call.arguments)
                origin = args.get("origin")
                destination = args.get("destination")
                date = args.get("date")
                flights = get_flights(origin, destination, date)
                results.append({"tool": "get_flights", "result": format_flights(flights)})
            elif tool_call.name == "book_flight":
                args = json.loads(tool_call.arguments)
                flight_id = args.get("flight_id")
                passenger_name = args.get("passenger_name")
                book_flight(flight_id, passenger_name)
                confirmation = f"Booking successful for {passenger_name} on flight {flight_id}"
                results.append({"tool": "book_flight", "result": confirmation})
            


        # handle file search 
        elif tool_call.type == "file_search":
            file_results = getattr(tool_call, "tool_call", None)
            if file_results and isinstance(file_results, list):
                file_text = "\n".join(str(item) for item in file_results)
                results.append({"tool": "file_search", "result": file_text})
            else:
                results.append({"tool": "file_search", "result": "No file search results found."})
        
        # handle web search preview
        elif tool_call.type == "web_search_preview":
            logging.info(f"Tool call type: {tool_call.type}")
            web_results = getattr(tool_call, "tool_call", None)
            if web_results and isinstance(web_results, list):
                web_text = "\n".json(str(item) for item in web_results)
                results.append({"tool": "web_search_preview", "result": web_text})
            else:
                results.append({"tool": "web_search_preview", "result": "No web search results found."})

        # handle normal assistant message
        elif hasattr(tool_call, "content"):  
            print("This is a normal assistant message")
            content = tool_call.content
            if isinstance(content, list) and len(content) > 0:
                text = content[0].text
                results.append({"tool": "assistant_message", "result": text})   
            elif isinstance(content, str):
                results.append({"tool": "assistant_message", "result": content})   

    # return combined results
    if results:
        return "\n".join(r.get("result", "") for r in results) 
    else:
        return "No valid respone generated."       

    

if __name__ == "__main__":
    app.run(debug=True)
 