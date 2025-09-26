🧳 Travel and Tourism Portal (FastAPI)

✨ Overview
A backend-driven travel and tourism portal built with FastAPI, designed to handle user authentication, destination listings, and booking operations. This project demonstrates modular API design, secure authentication, and clean architecture—perfect for showcasing backend development skills.

🚀 Features
- 🔐 User Authentication: Register and login endpoints using OAuth2
- 🗺️ Destination Management: Add, update, and retrieve travel destinations
- 📅 Booking System: Placeholder for booking logic (coming soon)
- 📦 Modular Routing: Clean separation of concerns via FastAPI routers
- 🧪 Testable Architecture: Ready for integration with pytest and Swagger UI

🛠️ Tech Stack
- Backend: Python, FastAPI
- Auth: OAuth2PasswordBearer, Pydantic models
- Database: SQLite (can be swapped for PostgreSQL)
- Dev Tools: VS Code, Git, GitHub
- Environment: Virtualenv, requirements.txt

📂 Project Structure
travel_and_tourism_project/
│
├── app/
│   ├── api/
│   │   └──  auth.py
│   ├──core/
│   │   └──  config.py
│   ├──db
│   ├──schemas
│   └── main.py
├── venv/ (excluded via .gitignore)
├── requirements.txt
├── README.md
└── .gitignore



🧪 How to Run Locally
# Clone the repo
git clone https://github.com/GrimmSmith/travel-and-tourism-portal.git
cd travel_and_tourism_project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app
uvicorn app.main:app --reload



📌 Status
✅ Auth router implemented
🔧 Destination and booking routers in progress
📄 Documentation and testing planned for final phase

🧠 What This Project Demonstrates
- Backend API design using FastAPI
- Secure user authentication
- Clean, modular code structure
- Professional documentation and GitHub workflow

