from flask import Flask, render_template, request, redirect
import pymysql
import os
from dotenv import load_dotenv
from discordwebhook import Discord

# Load environment variables
load_dotenv()

token = os.getenv('TOKEN')
disc = Discord(url=os.getenv('Trafic_webhook'))
disc2 = Discord(url=os.getenv('hospital_webhook'))

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="AmbulanceAlertingSystem"
        )
        cursor = db.cursor()

        sql = "SELECT proffession FROM user WHERE email_id=%s and password=%s;"
        val = (email, password)
        cursor.execute(sql, val)
        result = cursor.fetchall()

        if len(result) != 0:
            if result[0][0] == "hpt":
                return redirect("/hospital")
            elif result[0][0] == "trp":
                return redirect("/traffic-police")
            else:
                return redirect('/ambulance-drive')
        else:
            return render_template('index.html', password="False")

    return render_template('index.html')


# ---------------- ADMIN ----------------
@app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("Email")
        proffession = request.form.get("proffession")
        password = request.form.get("password")

        db = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="AmbulanceAlertingSystem"
        )
        cursor = db.cursor()

        sql = "INSERT INTO user(name,Email_Id,proffession,password) VALUES(%s,%s,%s,%s);"
        val = (name, email, proffession, password)
        cursor.execute(sql, val)
        db.commit()

        if proffession == 'trp':
            location = request.form.get("location")
            Discord_uname = request.form.get("d_name")
            from1 = request.form.get("from1")
            to1 = request.form.get("to1")

            sql = "INSERT INTO trafficsignal(f_rom,t_o,location,name,s_s_status,discord_name) VALUES(%s,%s,%s,%s,1,%s)"
            val = (from1, to1, location, name, Discord_uname)
            cursor.execute(sql, val)
            db.commit()

        elif proffession == "hpt":
            hospital_name = request.form.get("hospital")
            ready_to_attend = int(request.form.get("attendpatient"))
            discord_name_d = request.form.get("d_name-d")
            hpt_location = request.form.get("hospitallocation")

            sql = "INSERT INTO hospital(h_discord_name,hospital_name,accept_patient,location) VALUES(%s,%s,%s,%s)"
            val = (discord_name_d, hospital_name, ready_to_attend, hpt_location)
            cursor.execute(sql, val)
            db.commit()

        return "<h1>Record added Successfully</h1>"

    return render_template('Admin-Page.html')


# ---------------- HOSPITAL ----------------
@app.route('/hospital', methods=['GET', 'POST'])
def hospital():
    db = pymysql.connect(host="localhost", user="root", password="", database="AmbulanceAlertingSystem")
    cursor = db.cursor()

    cursor.execute('SELECT hospital_name,accept_patient FROM hospital')
    hospital_name_hp = cursor.fetchall()

    if request.method == 'POST':
        hospital_name_get = request.form.get('hospital_name_hp')
        ap_accept_patient = request.form.get('accept_patient')

        sql = f'UPDATE hospital SET accept_patient={ap_accept_patient} WHERE hospital_name="{hospital_name_get}"'
        cursor.execute(sql)
        db.commit()

    return render_template('hospital.html', hospital_name_hp=hospital_name_hp)


# ---------------- TRAFFIC ----------------
@app.route('/traffic-police', methods=['GET', 'POST'])
def traffic_poice():
    db = pymysql.connect(host="localhost", user="root", password="", database="AmbulanceAlertingSystem")
    cursor = db.cursor()

    cursor.execute('SELECT DISTINCT location,s_s_status FROM trafficsignal')
    traffic_police_tp = cursor.fetchall()

    if request.method == 'POST':
        traffic_location_tp = request.form.get('traffic_name_tp')
        signal_statu_tp = request.form.get('Signal_Status')

        sql = f'UPDATE trafficsignal SET s_s_status={signal_statu_tp} WHERE location="{traffic_location_tp}"'
        cursor.execute(sql)
        db.commit()

    return render_template('traffic_police.html', traffic_list=traffic_police_tp)


# ---------------- AMBULANCE ----------------
@app.route('/ambulance-drive', methods=["GET", "POST"])
def ambulancepage():
    db = pymysql.connect(host="localhost", user="root", password="", database="AmbulanceAlertingSystem")
    cursor = db.cursor()

    cursor.execute('SELECT f_rom,t_o from trafficsignal')
    fromlist = cursor.fetchall()

    if request.method == "POST":
        route_from = request.form.get("ambulancedriver-from")
        route_to = request.form.get("ambulancedriver-to")

        sql = f"SELECT location,name,s_s_status,discord_name FROM trafficsignal WHERE f_rom='{route_from}' AND t_o='{route_to}'"
        cursor.execute(sql)
        signal_details = cursor.fetchall()

        sql = f"SELECT hospital_name,accept_patient FROM hospital where location='{route_to}'"
        cursor.execute(sql)
        hospital_details = cursor.fetchall()

        # Send Discord alerts
        disc2.post(content=f"A patient is coming to {route_to}")
        for s in signal_details:
            disc.post(content=f"Ambulance is coming in {s[0]}")

        return render_template('Ambulance_driver_Page.html',
                               signal_details=signal_details,
                               fromlist=fromlist,
                               hospital_details=hospital_details)

    return render_template('Ambulance_driver_Page.html', fromlist=fromlist)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)