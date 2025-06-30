🚀 NASA Asteroid Tracker 🌠
A Streamlit-based web application that visualizes data from NASA's Near-Earth Object (NEO) database. Explore asteroid approach events, filter based on multiple criteria, and execute SQL queries for custom insights.

🧠 Features
🔎 Filter Criteria Page

Filter asteroids by magnitude, diameter, velocity, hazard status, date range, and astronomical distance.

Real-time updates with custom sliders and controls.

Display matching asteroids in a responsive data table.

📊 Query Page

Select from a list of 15 pre-built SQL queries.

Understand asteroid trends like:

Top 10 fastest asteroids

Most hazardous objects

Monthly asteroid counts

Objects brighter than magnitude threshold, etc.

🎯 Sidebar Navigation

Seamlessly switch between Filter Criteria and Queries.

📁 Project Structure
bash
Copy
Edit
📦 nasa-asteroid-tracker
├── streamlit_app.py          # Main Streamlit app
├── Neo.py                    # Main app for fetching data from api and uploading it into DB
└── README.md                 # Project documentation
⚙️ How to Run
🐍 Step 1: Set up environment
Make sure you have Python 3.8+ installed.

bash
Copy
Edit
pip install streamlit pandas
📂 Step 2: Clone or download this repository
bash
Copy
Edit
git clone https://github.com/YuvanVarshith/NASA-Asteroid-Tracker.git
cd nasa-asteroid-tracker
▶️ Step 3: Run the app
bash
Copy
Edit
streamlit run streamlit_app.py
Open http://localhost:8501 in your browser.

🧮 Data Source
NASA Near-Earth Object Web Service (NeoWs)

Data stored locally in neo_database.db (SQLite)

📚 Example SQL Queries Included
Count of approaches per asteroid

Average velocity by asteroid

Fastest asteroid ever

Approaches closer than 1 Lunar Distance

Objects brighter than magnitude 15

Most active approach months
...and more!

💡 Future Enhancements
🌐 Live API integration with NASA NeoWs

📈 Interactive charts (velocity, diameter, hazard trend)

🔔 Notifications for upcoming close approaches

🙌 Acknowledgments
Thanks to NASA's Open APIs and the Streamlit community for enabling such projects.