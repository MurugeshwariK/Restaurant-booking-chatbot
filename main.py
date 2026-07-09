from groq import Groq
import json


client = Groq(
  api_key="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"
   
)


def understand_message(message):

    prompt = f"""
You are a restaurant booking AI assistant.

Understand the user message and return JSON only.
No extra text. No markdown. Just raw JSON.

Always return all these fields — never remove any key:

{{
  "intent": "",
  "location": "",
  "restaurant": "",
  "guests": "",
  "date": "",
  "time": "",
  "booking_id": ""
}}

Intent values:
- SEARCH   → user wants to find/see restaurants
- BOOK     → user wants to make a new booking
- MODIFY   → user wants to change an existing booking
- CANCEL   → user wants to cancel a booking
- CHECK    → user wants to check availability
- FAQ      → general question

IMPORTANT: Extract ALL information from the message even if spelling is wrong.
"i wnat book pizza world for 5 people at 5 pm on 8 june 2026" means:
- intent: BOOK
- restaurant: Pizza World
- guests: 5
- time: 5 PM
- date: 8 June 2026

Examples:

User: show restaurants
Output:
{{"intent":"SEARCH","location":"","restaurant":"","guests":"","date":"","time":"","booking_id":""}}

User: book Pizza World for 4 people at 7 PM on 25 Dec 2024
Output:
{{"intent":"BOOK","location":"","restaurant":"Pizza World","guests":"4","date":"25 Dec 2024","time":"7 PM","booking_id":""}}

User: i wnat book pizza world for 5 people at 5 pm on 8 june 2026
Output:
{{"intent":"BOOK","location":"","restaurant":"Pizza World","guests":"5","date":"8 June 2026","time":"5 PM","booking_id":""}}

User: cancel booking TB12345
Output:
{{"intent":"CANCEL","location":"","restaurant":"","guests":"","date":"","time":"","booking_id":"TB12345"}}

User: modify my booking TB54321
Output:
{{"intent":"MODIFY","location":"","restaurant":"","guests":"","date":"","time":"","booking_id":"TB54321"}}

User: check availability in Chennai for 3 people
Output:
{{"intent":"CHECK","location":"Chennai","restaurant":"","guests":"3","date":"","time":"","booking_id":""}}

Message:
{message}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    return json.loads(raw)