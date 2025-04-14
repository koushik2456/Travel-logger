def process_query(query: str):
    # Mocking Groq response for now
    # Replace with Groq API logic later
    if "youtube" in query.lower():
        return {
            "type": "link",
            "content": "https://www.youtube.com/watch?v=sample123",
            "message": "You watched this around 6 PM yesterday!"
        }
    elif "how much time" in query.lower():
        return {
            "type": "stats",
            "content": "You spent 2 hours on YouTube yesterday."
        }
    else:
        return {
            "type": "text",
            "content": "I couldn't understand that. Try asking differently!"
        }
