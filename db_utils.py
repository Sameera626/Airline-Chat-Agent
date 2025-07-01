import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return pyodbc.connect(
        driver='{SQL Server}',
        server=os.getenv("SQL_SERVER"),
        database=os.getenv("SQL_DATABASE"),
        trusted_connection='yes'
    )

def get_flights(origin, destination, date):

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT origin, destination, date, seats_available FROM flights WHERE origin=? AND destination=? AND date=?",
            (origin, destination, date)
        )
        flights = cursor.fetchall()
        return flights
    except Exception as e:
        # print(f"Database error: {e}")
        raise Exception(f"Failed to fetch flights: {e}")
        # return []
    finally:
        conn.close() 

def format_flights(flights):
    if not flights:
        return "No flights found."
    return "\n" .join(f"{idx + 1}. {flight.origin} -> {flight.destination} on {flight.date} ({flight.seats_available} seats left)"
            for idx, flight in enumerate(flights))
  
def book_flight(flight_id, passenger_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT seats_available FROM flights WHERE id=?", (flight_id,))
        seats = cursor.fetchone()[0]

        if seats > 0:
            cursor.execute("INSERT INTO bookings (flight_id, passenger_name) VALUES (?, ?)", (flight_id, passenger_name))
            cursor.execute("UPDATE flights SET seats_available=? WHERE id=?", (seats-1, flight_id))
            conn.commit()
            return True
        return False
    
    except Exception as e:
        print(f"Booking error: {e}")
        return False
    finally:
        conn.close()