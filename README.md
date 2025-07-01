# Airline Chat Agent

A full-stack AI-powered airline assistant that helps users search for flights, book tickets, get weather updates, and answer policy/FAQ questions using OpenAI's function calling and file search tools.

---

## Features

- **Flight Search:** Find available flights between cities on specific dates.
- **Flight Booking:** Book a flight for a passenger.
- **Weather Info:** Get current weather for any city.
- **Policy & FAQ Search:** Ask questions about airline policies, with answers retrieved from uploaded documents using OpenAI file search.
- **Modern Frontend:** Built with Next.js and React.
- **Robust Backend:** Flask backend with modular structure and SQL Server database integration.

---

## Project Structure

```
airline-chat-agent/
├── app.py                       # Flask application entry point
├── db_utils.py                  # Database utility functions
├── weather_utils.py             # Weather API utility
├── create_vector_store.py       # Script to upload files and create OpenAI vector store
├── airline_policies.pdf         # Example policy/FAQ document
├── .env                         # Environment variables
├── .gitignore
├── Readme.md                    # Project documentation
```

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/airline-chat-agent.git
cd airline-chat-agent
```

### 2. Backend Setup

- **Install dependencies:**
  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

- **Configure environment variables:**  
  Create a `.env` file in the root directory with:
  ```
  OPENAI_API_KEY=your_openai_api_key
  OPENWETHER_API_KEY=your_openweather_api_key
  SQL_SERVER=your_sql_server
  SQL_DATABASE=airline-chat-agent
  ```

- **Set up the database:**
  - Ensure your SQL Server is running and the database/schema is created.
  - Use any provided `schema.sql` or `sample_data.sql` scripts if available.

- **Upload policy/FAQ documents and create a vector store:**
  ```sh
  python create_vector_store.py
  ```
  Use the printed `vector_store_id` in your `app.py` file's file search tool config.

- **Run the backend:**
  ```sh
  python app.py
  ```

---

## Usage

- **Chat with the assistant** to search flights, book tickets, get weather, or ask policy questions via the `/chat` endpoint.
- **Flight and booking data** are managed in your SQL database.
- **Policy/FAQ answers** are retrieved from your uploaded documents using OpenAI file search.

---

## API Endpoints

- `POST /chat`  
  **Request:**  
  ```json
  { "query": "Your question here" }
  ```
  **Response:**  
  Plain text answer from the assistant.

---

## Environment Variables

- `OPENAI_API_KEY` – Your OpenAI API key
- `OPENWETHER_API_KEY` – Your OpenWeatherMap API key
- `SQL_SERVER` – Your SQL Server instance
- `SQL_DATABASE` – Database name

---

## License

MIT License

---

## Acknowledgements

- [OpenAI](https://platform.openai.com/)
- [Flask](https://flask.palletsprojects.com/)
- [OpenWeatherMap](https://openweathermap.org/)

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like