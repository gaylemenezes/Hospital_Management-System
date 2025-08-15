import mysql.connector

db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="hospital"
)

def get_appointments(doctor_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.patient_id, p.name AS patient_name, a.appointment_date, a.appointment_time 
        FROM appointments a
        JOIN patient p ON a.patient_id = p.id
        WHERE a.doctor_id = %s AND a.status = 'scheduled'
    """, (doctor_id,))
    appointments = cursor.fetchall()
    cursor.close()
    return appointments
'''
def get_appointments(doctor_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT patient_name, appointment_date, appointment_time 
        FROM appointments 
        WHERE doctor_id = %s AND status = 'scheduled'
    """, (doctor_id,))
    appointments = cursor.fetchall()
    cursor.close()
    cursor.close()
    return appointments
'''

def get_patient_appointments(patient_id):
    cursor =db.cursor(dictionary= True)
    cursor.execute("""
        SELECT d.name AS doctor_name, a.appointment_date, a.appointment_time 
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.patient_id = %s AND a.status = 'scheduled'
    """, (patient_id,))
    appointments = cursor.fetchall()
    cursor.close()
    return appointments

def get_cursor():
    return db.cursor()
