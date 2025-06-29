# 🚑 Ambulance Alerting System

A real-time web-based Ambulance Alerting System designed to facilitate emergency services through better coordination between ambulance drivers, nearby hospitals, and traffic authorities using live location tracking and smart routing.

---

## 🎯 Objective

To reduce ambulance delays during emergencies by utilizing real-time location, map-based routing, and hospital discovery features. This system alerts concerned authorities and provides optimal routes for fast and efficient patient transport.

---

## 🛠 Tech Stack

- *Frontend:* HTML, CSS
- *Backend:* Python (Flask)
- *Database:* MySQL
- *Map Integration:* MapMyIndia API (Direction + Nearby Search)
- *Extras:* Discord Webhook (optional for alert messages)

---

## ✨ Key Features

- 🔐 Role-based login system (Ambulance driver, Hospital, etc.)
- 📍 Real-time map view with hospital locations
- 🏥 Nearby hospital search using MapMyIndia APIs
- 🚨 Alerts & directions to emergency spots
- 📊 User-friendly UI with dropdown-based location selection

---

## 📸 Demo Screenshots

### 🔹 Login Page
![Login Page](screenshots/login.png)

### 🔹 Driver Map View with Hospital Search
![Driver Page](screenshots/map1.png)

### 🔹 Alternate View – Different Hospitals on Map
![Map View 2](screenshots/map2.png)

---

## 📁 Folder Structure
ambulance-alerting-system-main/
├── Ambulance-Alerting-System.py
├── README.md
├── templates/
├── static/
├── screenshots/
│   ├── login.png
│   ├── map1.png
│   └── map2.png


---

## ▶️ How to Run Locally

1. Clone the repository or download ZIP
2. Install required packages:
```bash
pip install flask mysql-connector-python
3.run locally
python Ambulance-Alerting-System.py

📦 Requirements
flask
mysql-connector-python

🔗 GitHub Repository
https://github.com/shivanibaravkar/ambulance-alerting-system

🙌 Author
Shivani Baravkar
Final Year CSE + DS Student
Passionate about real-world problem-solving with technology.


