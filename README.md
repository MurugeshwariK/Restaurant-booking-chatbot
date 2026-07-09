# 🍽️ Restaurant Table Booking Chatbot

A full-stack AI-powered chatbot that allows users to **search, book, modify, and cancel** restaurant table reservations through a natural language chat interface.

---

## 🚀 Live Demo

> Type messages like:
> - *"Book a table at Pizza World for 4 people at 7 PM on 25 Dec"*
> - *"Show me restaurants in Chennai"*
> - *"Cancel my booking TB47382"*

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI / NLP | Groq API (LLaMA 3.1 model) |
| Database | MySQL |

---

## 📁 Project Structure

```
restaurant_bot/
│
├── frontend/
│   ├── index.html       # Chat UI
│   ├── style.css        # Styling
│   └── script.js        # Sends messages to backend, shows replies
│
├── backend/
│   ├── main.py          # FastAPI server — receives HTTP requests
│   ├── chatbot.py       # Core logic — handles intents and state
│   ├── groq_ai.py       # Groq AI integration — understands user messages
│   └── database.py      # MySQL connection
│
└── database/
    └── restaurant.sql   # Database schema + sample data
```

---

## ⚙️ How It Works

```
User types message
       ↓
JavaScript (script.js) sends HTTP GET request to FastAPI
       ↓
main.py receives request → calls chatbot.py
       ↓
chatbot.py sends message to Groq AI (groq_ai.py)
       ↓
Groq AI returns intent as JSON  (BOOK / CANCEL / SEARCH / MODIFY / FAQ)
       ↓
chatbot.py runs SQL queries via database.py
       ↓
Reply sent back to browser → shown in chat
```

---

## 🗄️ Database Tables

### `restaurants`
Stores restaurant information.
| Column | Type | Description |
|---|---|---|
| id | INT | Primary key |
| name | VARCHAR | Restaurant name |
| location | VARCHAR | City |
| cuisine | VARCHAR | Food type |
| rating | FLOAT | Rating out of 5 |
| opening_time | VARCHAR | Working hours |
| menu | TEXT | Food items |
| parking | VARCHAR | Parking availability |

### `restaurant_tables`
Stores seating capacity for each restaurant.
| Column | Type | Description |
|---|---|---|
| id | INT | Primary key |
| restaurant_id | INT | Foreign key → restaurants |
| capacity | INT | Number of seats |
| status | VARCHAR | Available / Booked |

### `bookings`
Stores all customer reservations.
| Column | Type | Description |
|---|---|---|
| id | INT | Primary key |
| booking_code | VARCHAR | Unique ID e.g. TB47382 |
| restaurant | VARCHAR | Restaurant name |
| booking_date | VARCHAR | Date of booking |
| time | VARCHAR | Time of booking |
| guests | INT | Number of guests |
| status | VARCHAR | Confirmed / Cancelled |

---

## 🔧 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/restaurant-bot.git
cd restaurant-bot
```

### 2. Install Python dependencies
```bash
pip install fastapi uvicorn mysql-connector-python groq
```

### 3. Setup the MySQL database
```bash
mysql -u root -p
SOURCE database/restaurant.sql;
```

### 4. Add your Groq API key
In `backend/groq_ai.py`, replace:
```python
api_key="your_groq_api_key_here"
```
Get your free API key at: https://console.groq.com

### 5. Update database credentials
In `backend/database.py`, update:
```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="restaurant_bot"
)
```

### 6. Run the backend server
```bash
cd backend
uvicorn main:app --reload
```
Server runs at: `http://127.0.0.1:8000`

### 7. Open the frontend
Open `frontend/index.html` directly in your browser.

---

## 💬 Supported Commands

| What you type | What the bot does |
|---|---|
| "Show restaurants in Chennai" | Lists restaurants by city |
| "Book a table at Spice Garden" | Starts booking flow |
| "Cancel booking TB47382" | Cancels a reservation |
| "Modify my booking TB47382" | Updates restaurant or time |
| "What is the menu at Pizza World?" | Shows menu / FAQ info |
| "Is parking available at Food Palace?" | Answers FAQ |

---

## 🧠 Key Concepts Used

- **FastAPI** — lightweight Python web framework for building REST APIs
- **Groq AI + LLaMA 3.1** — AI model to understand natural language and extract booking intent as JSON
- **State Dictionary** — tracks multi-step conversations (e.g. asking restaurant → date → time → guests one by one)
- **MySQL** — stores all restaurant and booking data
- **CORS Middleware** — allows the HTML frontend to communicate with the Python backend
---





This project is open source and available under the [MIT License](LICENSE).
