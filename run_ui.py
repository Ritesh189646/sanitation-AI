import webbrowser
import threading
import time
from app import app

def open_browser():
    time.sleep(1.5)
    print("🌐 Opening Sanitation AI Web Dashboard in your browser...")
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("=" * 65)
    print("   SANITATION AI - YOLO VISION & CLEANLINESS DASHBOARD")
    print("=" * 65)
    print(" Server starting on http://127.0.0.1:5000 ...")
    
    # Launch browser thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask server
    app.run(host="127.0.0.1", port=5000, debug=False)
