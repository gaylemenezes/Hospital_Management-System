from flask import Flask, render_template,request,redirect,url_for,session,jsonify
from models.database import db, get_cursor
from models.database import get_appointments, get_patient_appointments
from chatbot.chatbot import get_chat_response


app=Flask(__name__, template_folder='templates')
app.secret_key="your_super_secret_key"


@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/doctor/dashboard")
def doctor_dashboard():
    if session.get("role")!= "doctor":
        return redirect(url_for("login"))
    doctor_id = 1 
    appointments = get_appointments(doctor_id)
    return render_template("doctor_dashboard.html", name=session.get("user_name"), appointments=appointments)
    

@app.route("/patient/dashboard")
def patient_dashboard():
    if session.get("role")!= "patient":
        return redirect(url_for("login"))
    patient_id = session.get('user_id')
    appointments = get_patient_appointments(patient_id)
    return render_template("patient_dashboard.html", name=session.get("user_name"), appointments=appointments)

@app.route("/staff/dashboard")
def staff_dashboard():
    if session.get("role")!= "staff":
        return redirect(url_for("login"))
    cursor=get_cursor()
    cursor.execute('SELECT id, name from doctors')
    doctors = cursor.fetchall()
    cursor.close()
    return render_template("staff_dashboard.html", name=session.get("user_name"), doctors= doctors)

@app.route("/staff/schedule", methods=["POST"])
def staff_schedule():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    username = request.form["username"]
    password = request.form["password"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]

    cursor = get_cursor()

    # Check if patient exists
    cursor.execute('SELECT id FROM patient WHERE username=%s', (username,))
    patient = cursor.fetchone()

    if patient:
        patient_id = patient[0]
    else:
        # Clean phone number (digits only)
        phone = "".join(filter(str.isdigit, phone))

        # Insert new patient
        cursor.execute("""
            INSERT INTO patient (name, email, phone, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, username, password))
        db.commit()
        patient_id = cursor.lastrowid

    # Insert appointment
    cursor.execute("""
        INSERT INTO appointments (
            patient_name, appointment_date, appointment_time, doctor_id, status, patient_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, appointment_date, appointment_time, doctor_id, "scheduled", patient_id))

    db.commit()
    cursor.close()

    return redirect(url_for("staff_dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        role=request.form["role"]
        

        table_name = "doctors" if role == "doctor" else "patient" if role == "patient" else "staff"
        cursor=get_cursor()
        check_sql=f"select * from {table_name} where username=%s"
        cursor.execute(check_sql, (username,))
        user=cursor.fetchone()
        cursor.close()

        if user:
            db_password= user[5]
            if password==db_password:
                session["user_id"]= user[0]
                session["user_name"]=user[1]
                session["role"]= role
                
                if role == "patient":
                    return redirect(url_for("patient_dashboard"))
                elif role == "doctor":
                    return redirect(url_for("doctor_dashboard"))
                else:
                    return redirect(url_for("staff_dashboard"))
                
            return """
            <script>
                alert("Invalid username or password! Try again!")
                 window.location.href="/login";
            </script>
            """
        return """
        <script>
            alert(" Invalid username or password! Try again!");
            window.location.href = "/login";
        </script.
        """
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email= request.form["email"]
        phone=request.form["phone"]
        username=request.form["username"]
        password=request.form["password"]
        role=request.form["role"]

        if not role: 
            print(" Role is missing from form submission!")
        
        if not name: 
            print(" Name is missing from form submission!")
        if not email: 
            print(" Email is missing from form submission!")
        if not username: 
            print(" Username is missing from form submission!")

        if not password: 
            print(" Password is missing from form submission!")

       
        cursor= get_cursor()
        phone = "".join(filter(str.isdigit, phone))
        
        check_sql= 'Select * from {} WHERE email=%s or username=%s'.format("doctors" if role=="doctor" else "patient" if role== "patient" else "staff")


        cursor.execute(check_sql,(email,username))
        existing_user=cursor.fetchone()
        if existing_user:
            return """
            <script>
            alert("Email or username already exists! Try with another username or email")
            window.location.href="/login";
            </script>
            """

        insert_sql="Insert into {}(name, email,phone,username,password) values (%s,%s,%s,%s,%s)".format("doctors" if role=="doctor" else "patient" if role== "patient" else "staff")
        cursor.execute(insert_sql,(name,email,phone,username,password))
        db.commit()
        cursor.close()
        return """
        <script>
        alert("Registration successful!");
        window.location.href="/login";
        </script>
         """

    return render_template("register.html", error="Username or email already exists") 

@app.route("/doctor/add_report/<int:patient_id>", methods=["GET", "POST"])
def add_report(patient_id):
    if session.get("role") != "doctor":
        return redirect(url_for("login"))
    
    doctor_id= session.get("user_id")
    cursor=get_cursor()

    cursor.execute("SELECT name FROM patient WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()
    name = patient[0] if patient else "Unknown"

    if request.method=="POST":
        title= request.form["report_title"]
        chief_complaint = request.form["chief_complaint"]
        medical_history = request.form["medical_history"]
        examination = request.form["examination"]
        diagnosis = request.form["diagnosis"]
        treatment = request.form["treatment"]
        remarks = request.form["remarks"]
        description = f"""### Chief Complaint
{chief_complaint}

### Medical History
{medical_history}

### Examination Findings
{examination}

### Diagnosis
{diagnosis}

### Treatment Plan
{treatment}

### Remarks
{remarks}
"""
        
        

        insert_sql= """
           insert into reports(patient_id,doctor_id,report_date, report_title,report_description)
           values(%s, %s, CURDATE(), %s, %s)
        """

        cursor.execute(insert_sql, (patient_id, doctor_id, title, description))
        db.commit()
        cursor.close()
        return redirect(url_for("doctor_dashboard"))
    return render_template("add_report.html", patient_id=patient_id)

@app.route("/patient/view_reports")
def view_reports():
    if session.get("role") != 'patient':
        return redirect(url_for('login'))
    
    patient_id= session.get('user_id')
    cursor=get_cursor()
    cursor.execute("""
        SELECT report_date, report_title, report_description
        FROM reports
        WHERE patient_id = %s
        ORDER BY report_date DESC
    """, (patient_id,))
    reports= cursor.fetchall()
    cursor.close()
    return render_template("view_reports.html", reports=reports)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
     user_message = request.json['message']
     bot_response = get_chat_response(user_message)
     return jsonify({'response': bot_response})


if(__name__=="__main__"):
    app.run(debug=True)