from datetime import datetime

def get_screen_data():
    # This should use ScreenPipe in real project
    # For now, we simulate a screen data log
    return {
        "screenshots": [
            {
                "timestamp": str(datetime.now()),
                "link": "https://example.com/screenshot1.png"
            }
        ]
    }
