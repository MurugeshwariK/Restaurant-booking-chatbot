from database import cursor, db
from groq_ai import understand_message
import random


# Conversation state
state = {
    "action": None,
    "booking_id": None,
    "step": None
}

# Temporary booking data
booking_data = {
    "restaurant": None,
    "date": None,
    "time": None,
    "guests": None
}


def reset_state():
    state["action"] = None
    state["booking_id"] = None
    state["step"] = None
    booking_data["restaurant"] = None
    booking_data["date"] = None
    booking_data["time"] = None
    booking_data["guests"] = None


def get_all_restaurants():
    cursor.execute("SELECT * FROM restaurants")
    return cursor.fetchall()


def restaurant_list_text():
    hotels = get_all_restaurants()
    text = "Available Restaurants:\n\n"
    for h in hotels:
        text += f"""Name     : {h['name']}
Location : {h['location']}
Cuisine  : {h['cuisine']}
Rating   : {h['rating']}
Hours    : {h['opening_time']}
Parking  : {h['parking']}

----------------------------

"""
    return text


def generate_booking_id():
    return "TB" + str(random.randint(10000, 99999))


def do_confirm_booking():
    booking_id = generate_booking_id()

    cursor.execute(
        """
        INSERT INTO bookings
        (booking_code, restaurant, booking_date, time, guests, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            booking_id,
            booking_data["restaurant"],
            booking_data["date"],
            booking_data["time"],
            booking_data["guests"],
            "Confirmed"
        )
    )
    db.commit()

    result = f"""Booking Confirmed!

Booking ID  : {booking_id}
Restaurant  : {booking_data['restaurant']}
Date        : {booking_data['date']}
Time        : {booking_data['time']}
Guests      : {booking_data['guests']}
Status      : Confirmed

Please save your Booking ID: {booking_id}
You will need it to modify or cancel your booking."""

    reset_state()
    return result


def process_message(msg):

    text = msg.strip()


    # ==========================================
    # BOOK FLOW
    # ==========================================

    if state["action"] == "booking":

        if state["step"] == "restaurant":
            booking_data["restaurant"] = text

            if not booking_data["date"]:
                state["step"] = "date"
                return "What date would you like to book? (e.g. 25 Dec 2024)"
            if not booking_data["time"]:
                state["step"] = "time"
                return "What time? (e.g. 7:00 PM)"
            if not booking_data["guests"]:
                state["step"] = "guests"
                return "How many guests?"
            return do_confirm_booking()

        if state["step"] == "date":
            booking_data["date"] = text

            if not booking_data["time"]:
                state["step"] = "time"
                return "What time? (e.g. 7:00 PM)"
            if not booking_data["guests"]:
                state["step"] = "guests"
                return "How many guests?"
            return do_confirm_booking()

        if state["step"] == "time":
            booking_data["time"] = text

            if not booking_data["guests"]:
                state["step"] = "guests"
                return "How many guests?"
            return do_confirm_booking()

        if state["step"] == "guests":
            booking_data["guests"] = text
            return do_confirm_booking()


    # ==========================================
    # MODIFY FLOW
    # ==========================================

    if state["action"] == "modify":

        if state["step"] == "ask_id":

            booking_id = text.upper()

            cursor.execute(
                "SELECT * FROM bookings WHERE booking_code = %s",
                (booking_id,)
            )
            booking = cursor.fetchone()

            if not booking:
                reset_state()
                return f"Booking ID '{booking_id}' not found. Please check and try again."

            state["booking_id"] = booking_id
            state["step"] = "ask_details"

            restaurants = restaurant_list_text()

            return f"""Current Booking Details:
Restaurant : {booking['restaurant']}
Date       : {booking['booking_date']}
Time       : {booking['time']}
Guests     : {booking['guests']}

{restaurants}
Please enter the new restaurant name and new time.
Example: Spice Garden, 8:00 PM"""

        if state["step"] == "ask_details":

            data = understand_message(text)

            new_restaurant = data.get("restaurant") or text.split(",")[0].strip()
            new_time = data.get("time") or (text.split(",")[1].strip() if "," in text else "")

            cursor.execute(
                """
                UPDATE bookings
                SET restaurant = %s,
                    time = %s
                WHERE booking_code = %s
                """,
                (new_restaurant, new_time, state["booking_id"])
            )
            db.commit()

            result = f"""Booking Modified Successfully!

Booking ID  : {state['booking_id']}
Restaurant  : {new_restaurant}
New Time    : {new_time}
Status      : Confirmed"""

            reset_state()
            return result


    # ==========================================
    # CANCEL FLOW
    # ==========================================

    if state["action"] == "cancel":

        if state["step"] == "ask_id":

            booking_id = text.upper()

            cursor.execute(
                "SELECT * FROM bookings WHERE booking_code = %s",
                (booking_id,)
            )
            booking = cursor.fetchone()

            if not booking:
                reset_state()
                return f"Booking ID '{booking_id}' not found. Please check and try again."

            cursor.execute(
                "UPDATE bookings SET status = 'Cancelled' WHERE booking_code = %s",
                (booking_id,)
            )
            db.commit()

            result = f"""Booking Cancelled.

Booking ID  : {booking_id}
Restaurant  : {booking['restaurant']}
Date        : {booking['booking_date']}
Time        : {booking['time']}
Guests      : {booking['guests']}
Status      : Cancelled

Your booking has been successfully cancelled."""

            reset_state()
            return result


    # ==========================================
    # AI UNDERSTANDS INTENT
    # ==========================================

    data = understand_message(msg)
    intent = data.get("intent", "")


    # ──────────────────
    # SHOW RESTAURANTS
    # ──────────────────

    if intent == "SEARCH":

        location = data.get("location", "")

        if location:
            cursor.execute(
                "SELECT * FROM restaurants WHERE LOWER(location) = LOWER(%s)",
                (location,)
            )
        else:
            cursor.execute("SELECT * FROM restaurants")

        hotels = cursor.fetchall()

        if not hotels:
            return "No restaurants found in that location."

        reply = "Restaurants Found:\n\n"
        for h in hotels:
            reply += f"""Name     : {h['name']}
Location : {h['location']}
Cuisine  : {h['cuisine']}
Rating   : {h['rating']}
Hours    : {h['opening_time']}
Menu     : {h['menu']}
Parking  : {h['parking']}

----------------------------

"""
        return reply


    # ──────────────────
    # CHECK AVAILABILITY
    # ──────────────────

    if intent == "CHECK":

        location = data.get("location", "")
        guests = data.get("guests", "")

        if location:
            cursor.execute(
                "SELECT * FROM restaurants WHERE LOWER(location) = LOWER(%s)",
                (location,)
            )
        else:
            cursor.execute("SELECT * FROM restaurants")

        hotels = cursor.fetchall()

        if not hotels:
            return "No restaurants found in that location."

        reply = "Available Restaurants"
        if location:
            reply += f" in {location}"
        if guests:
            reply += f" for {guests} guests"
        reply += ":\n\n"

        for h in hotels:
            reply += f"""Name     : {h['name']}
Location : {h['location']}
Cuisine  : {h['cuisine']}
Hours    : {h['opening_time']}
Parking  : {h['parking']}

----------------------------

"""
        reply += "To book a table, type: book table"
        return reply


    # ──────────────────
    # BOOK TABLE
    # ──────────────────

    if intent == "BOOK":

        restaurant = data.get("restaurant", "")
        date       = data.get("date", "")
        time       = data.get("time", "")
        guests     = data.get("guests", "")

        if restaurant and date and time and guests:

            booking_id = generate_booking_id()

            cursor.execute(
                """
                INSERT INTO bookings
                (booking_code, restaurant, booking_date, time, guests, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (booking_id, restaurant, date, time, guests, "Confirmed")
            )
            db.commit()

            return f"""Booking Confirmed!

Booking ID  : {booking_id}
Restaurant  : {restaurant}
Date        : {date}
Time        : {time}
Guests      : {guests}
Status      : Confirmed

Please save your Booking ID: {booking_id}
You will need it to modify or cancel your booking."""

        state["action"] = "booking"
        booking_data["restaurant"] = restaurant or None
        booking_data["date"]       = date or None
        booking_data["time"]       = time or None
        booking_data["guests"]     = guests or None

        if not restaurant:
            state["step"] = "restaurant"
            return restaurant_list_text() + "\nWhich restaurant would you like to book?"

        if not date:
            state["step"] = "date"
            return f"Great! Booking at {restaurant}.\nWhat date would you like? (e.g. 25 Dec 2024)"

        if not time:
            state["step"] = "time"
            return f"Got it! Booking at {restaurant} on {date}.\nWhat time? (e.g. 7:00 PM)"

        if not guests:
            state["step"] = "guests"
            return "Almost done!\nHow many guests?"


    # ──────────────────
    # MODIFY BOOKING
    # ──────────────────

    if intent == "MODIFY":

        booking_id = data.get("booking_id", "").upper()

        if booking_id:
            cursor.execute(
                "SELECT * FROM bookings WHERE booking_code = %s",
                (booking_id,)
            )
            booking = cursor.fetchone()

            if not booking:
                return f"Booking ID '{booking_id}' not found. Please check and try again."

            state["action"] = "modify"
            state["booking_id"] = booking_id
            state["step"] = "ask_details"

            restaurants = restaurant_list_text()

            return f"""Current Booking Details:
Restaurant : {booking['restaurant']}
Date       : {booking['booking_date']}
Time       : {booking['time']}
Guests     : {booking['guests']}

{restaurants}
Please enter the new restaurant name and new time.
Example: Spice Garden, 8:00 PM"""

        state["action"] = "modify"
        state["step"] = "ask_id"
        return """Modify Booking

Please enter your Booking ID.
Example: TB12345"""


    # ──────────────────
    # CANCEL BOOKING
    # ──────────────────

    if intent == "CANCEL":

        booking_id = data.get("booking_id", "").upper()

        if booking_id:
            cursor.execute(
                "SELECT * FROM bookings WHERE booking_code = %s",
                (booking_id,)
            )
            booking = cursor.fetchone()

            if not booking:
                return f"Booking ID '{booking_id}' not found. Please check and try again."

            cursor.execute(
                "UPDATE bookings SET status = 'Cancelled' WHERE booking_code = %s",
                (booking_id,)
            )
            db.commit()

            return f"""Booking Cancelled.

Booking ID  : {booking_id}
Restaurant  : {booking['restaurant']}
Date        : {booking['booking_date']}
Time        : {booking['time']}
Guests      : {booking['guests']}
Status      : Cancelled

Your booking has been successfully cancelled."""

        state["action"] = "cancel"
        state["step"] = "ask_id"
        return """Cancel Booking

Please enter your Booking ID.
Example: TB12345"""


    # ──────────────────
    # FAQ
    # ──────────────────

    if intent == "FAQ":

        question = msg.lower()

        cursor.execute("SELECT * FROM restaurants")
        all_hotels = cursor.fetchall()

        # Check if user asked about a specific restaurant
        specific = None
        for h in all_hotels:
            if h['name'].lower() in question:
                specific = h
                break

        hotels = [specific] if specific else all_hotels

        if any(word in question for word in ["hour", "hours", "open", "opening", "close", "closing", "when", "timing", "timings"]):
            reply = "Restaurant Hours:\n\n"
            for h in hotels:
                reply += f"""Name  : {h['name']}
Hours : {h['opening_time']}

"""
            return reply

        if any(word in question for word in ["menu", "food", "dish", "dishes", "serve", "cuisine", "eat", "items"]):
            reply = "Restaurant Menu:\n\n"
            for h in hotels:
                reply += f"""Name    : {h['name']}
Cuisine : {h['cuisine']}
Menu    : {h['menu']}

----------------------------

"""
            return reply

        if any(word in question for word in ["parking", "park", "car", "vehicle"]):
            reply = "Parking Information:\n\n"
            for h in hotels:
                reply += f"""Name    : {h['name']}
Parking : {h['parking']}

"""
            return reply

        if any(word in question for word in ["rating", "rate", "review", "best", "top", "good", "recommend"]):
            reply = "Restaurant Ratings:\n\n"
            for h in hotels:
                reply += f"""Name   : {h['name']}
Rating : {h['rating']}

"""
            return reply

        if any(word in question for word in ["location", "where", "address", "place", "city"]):
            reply = "Restaurant Locations:\n\n"
            for h in hotels:
                reply += f"""Name     : {h['name']}
Location : {h['location']}

"""
            return reply

        # General — show everything
        reply = "Restaurant Information:\n\n"
        for h in hotels:
            reply += f"""Name     : {h['name']}
Location : {h['location']}
Cuisine  : {h['cuisine']}
Rating   : {h['rating']}
Hours    : {h['opening_time']}
Menu     : {h['menu']}
Parking  : {h['parking']}

----------------------------

"""
        return reply


    # ──────────────────
    # FALLBACK
    # ──────────────────

    return """I can help you with:

Show Restaurants   - type: show restaurants
Book a Table       - type: book table
Check Availability - type: check availability
Modify Booking     - type: modify booking
Cancel Booking     - type: cancel booking
FAQ                - ask about hours, menu, parking, rating

What would you like to do?"""