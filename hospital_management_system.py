import os
import csv
import datetime
import random

# ══════════════════════════════════════════════════════════
#   FILE NAMES  (CSV files auto-created on first run)
# ══════════════════════════════════════════════════════════
PATIENTS_FILE     = "patients.csv"
DOCTORS_FILE      = "doctors.csv"
APPOINTMENTS_FILE = "appointments.csv"
BILLS_FILE        = "bills.csv"

# ══════════════════════════════════════════════════════════
#   CSV FIELD DEFINITIONS
# ══════════════════════════════════════════════════════════
P_FIELDS = ["id", "name", "age", "gender", "contact",
            "address", "blood_group", "admitted_on", "status"]

D_FIELDS = ["id", "name", "specialization", "contact", "available_days"]

A_FIELDS = ["id", "patient_id", "patient_name",
            "doctor_id", "doctor_name",
            "date", "time", "reason", "status"]

B_FIELDS = ["bill_id", "patient_id", "patient_name", "doctor_name",
            "date", "consultation", "medicine", "room", "tests", "total"]

# ══════════════════════════════════════════════════════════
#   UTILITY HELPERS
# ══════════════════════════════════════════════════════════
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def today():
    return datetime.date.today().strftime("%Y-%m-%d")

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d  %H:%M")

def gen_id(prefix):
    return f"{prefix}{random.randint(1000, 9999)}"

def line(char="─", width=58):
    print("  " + char * width)

def header(title):
    print()
    line("═")
    print(f"   🏥  {title}")
    line("═")

def pause():
    input("\n  Press Enter to continue...")

# ══════════════════════════════════════════════════════════
#   CSV READ / WRITE
# ══════════════════════════════════════════════════════════
def read_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(filename, fieldnames, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def append_csv(filename, fieldnames, row):
    exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            w.writeheader()
        w.writerow(row)

# ══════════════════════════════════════════════════════════
#   SEED DEFAULT DOCTORS  (runs only once)
# ══════════════════════════════════════════════════════════
def seed_doctors():
    if not os.path.exists(DOCTORS_FILE):
        defaults = [
            {"id": "D1001", "name": "Dr. Arjun Mehta",
             "specialization": "Cardiologist",   "contact": "9000000001", "available_days": "Mon–Fri"},
            {"id": "D1002", "name": "Dr. Priya Sharma",
             "specialization": "Neurologist",    "contact": "9000000002", "available_days": "Mon, Wed, Fri"},
            {"id": "D1003", "name": "Dr. Rahul Verma",
             "specialization": "Orthopedic",     "contact": "9000000003", "available_days": "Tue, Thu, Sat"},
            {"id": "D1004", "name": "Dr. Sneha Kapoor",
             "specialization": "Pediatrician",   "contact": "9000000004", "available_days": "Mon–Fri"},
            {"id": "D1005", "name": "Dr. Vikram Nair",
             "specialization": "Dermatologist",  "contact": "9000000005", "available_days": "Wed, Sat"},
        ]
        write_csv(DOCTORS_FILE, D_FIELDS, defaults)
        print("  ✅  5 default doctors loaded.")

# ══════════════════════════════════════════════════════════
#   ██████  PATIENT MODULE
# ══════════════════════════════════════════════════════════

def register_patient():
    header("Register New Patient")
    pid     = gen_id("P")
    name    = input("  Full Name         : ").strip()
    age     = input("  Age               : ").strip()
    gender  = input("  Gender (M / F / O): ").strip().upper()
    contact = input("  Contact Number    : ").strip()
    address = input("  Address           : ").strip()
    blood   = input("  Blood Group       : ").strip().upper()

    row = {
        "id": pid, "name": name, "age": age, "gender": gender,
        "contact": contact, "address": address, "blood_group": blood,
        "admitted_on": today(), "status": "Admitted"
    }
    append_csv(PATIENTS_FILE, P_FIELDS, row)
    print(f"\n  ✅  Patient registered successfully!")
    print(f"  📋  Patient ID : {pid}  |  Name : {name}")
    pause()


def view_all_patients():
    header("All Patients")
    rows = read_csv(PATIENTS_FILE)
    if not rows:
        print("  No patients registered yet.")
        pause()
        return
    print(f"\n  {'ID':<8} {'Name':<22} {'Age':<5} {'Gender':<8} {'Blood':<7} {'Status':<12} {'Admitted On'}")
    line()
    for r in rows:
        print(f"  {r['id']:<8} {r['name']:<22} {r['age']:<5} "
              f"{r['gender']:<8} {r['blood_group']:<7} {r['status']:<12} {r['admitted_on']}")
    print(f"\n  Total: {len(rows)} patient(s)")
    pause()


def search_patient():
    header("Search Patient")
    query = input("  Enter Patient ID or Name: ").strip().lower()
    rows  = read_csv(PATIENTS_FILE)
    hits  = [r for r in rows
             if query in r["id"].lower() or query in r["name"].lower()]
    if not hits:
        print("  ❌  No matching patient found.")
    else:
        for r in hits:
            line()
            print(f"  ID          : {r['id']}")
            print(f"  Name        : {r['name']}")
            print(f"  Age         : {r['age']}   |  Gender : {r['gender']}  |  Blood : {r['blood_group']}")
            print(f"  Contact     : {r['contact']}")
            print(f"  Address     : {r['address']}")
            print(f"  Admitted On : {r['admitted_on']}   |  Status : {r['status']}")
        line()
    pause()


def update_patient():
    header("Update Patient Record")
    pid  = input("  Enter Patient ID: ").strip()
    rows = read_csv(PATIENTS_FILE)
    found = False
    for r in rows:
        if r["id"] == pid:
            found = True
            print(f"\n  Editing record for: {r['name']}")
            print("  (Press Enter to keep current value)\n")
            r["name"]    = input(f"  Name    [{r['name']}]: ").strip()    or r["name"]
            r["age"]     = input(f"  Age     [{r['age']}]: ").strip()      or r["age"]
            r["contact"] = input(f"  Contact [{r['contact']}]: ").strip()  or r["contact"]
            r["address"] = input(f"  Address [{r['address']}]: ").strip()  or r["address"]
            r["status"]  = input(f"  Status  [{r['status']}] (Admitted/Discharged): ").strip() or r["status"]
    if found:
        write_csv(PATIENTS_FILE, P_FIELDS, rows)
        print("\n  ✅  Patient record updated.")
    else:
        print("  ❌  Patient ID not found.")
    pause()


def discharge_patient():
    header("Discharge Patient")
    pid  = input("  Enter Patient ID: ").strip()
    rows = read_csv(PATIENTS_FILE)
    found = False
    pname = ""
    for r in rows:
        if r["id"] == pid:
            if r["status"] == "Discharged":
                print("  ⚠️   Patient is already discharged.")
                pause()
                return
            r["status"] = "Discharged"
            pname = r["name"]
            found = True
    if found:
        write_csv(PATIENTS_FILE, P_FIELDS, rows)
        print(f"\n  ✅  {pname} has been discharged.")
        if input("  Generate bill now? (y / n): ").strip().lower() == "y":
            generate_bill(pid, pname)
    else:
        print("  ❌  Patient not found.")
    pause()


# ══════════════════════════════════════════════════════════
#   ██████  DOCTOR MODULE
# ══════════════════════════════════════════════════════════

def view_doctors():
    header("Doctors on Staff")
    rows = read_csv(DOCTORS_FILE)
    if not rows:
        print("  No doctors on record.")
        pause()
        return
    print(f"\n  {'ID':<8} {'Name':<22} {'Specialization':<20} {'Contact':<13} {'Available Days'}")
    line()
    for r in rows:
        print(f"  {r['id']:<8} {r['name']:<22} {r['specialization']:<20} "
              f"{r['contact']:<13} {r['available_days']}")
    print(f"\n  Total: {len(rows)} doctor(s)")
    pause()


def add_doctor():
    header("Add New Doctor")
    did  = gen_id("D")
    name = input("  Doctor Full Name    : ").strip()
    spec = input("  Specialization     : ").strip()
    cont = input("  Contact Number     : ").strip()
    days = input("  Available Days     : ").strip()
    row  = {"id": did, "name": name, "specialization": spec,
            "contact": cont, "available_days": days}
    append_csv(DOCTORS_FILE, D_FIELDS, row)
    print(f"\n  ✅  Doctor added!  ID: {did}  |  Name: {name}")
    pause()


def remove_doctor():
    header("Remove Doctor")
    did  = input("  Enter Doctor ID to remove: ").strip()
    rows = read_csv(DOCTORS_FILE)
    new  = [r for r in rows if r["id"] != did]
    if len(new) == len(rows):
        print("  ❌  Doctor ID not found.")
    else:
        write_csv(DOCTORS_FILE, D_FIELDS, new)
        print("  ✅  Doctor removed.")
    pause()


# ══════════════════════════════════════════════════════════
#   ██████  APPOINTMENT MODULE
# ══════════════════════════════════════════════════════════

def book_appointment():
    header("Book Appointment")
    patients = read_csv(PATIENTS_FILE)
    doctors  = read_csv(DOCTORS_FILE)

    if not patients:
        print("  ❌  No patients registered yet.")
        pause(); return
    if not doctors:
        print("  ❌  No doctors available.")
        pause(); return

    pid     = input("  Patient ID: ").strip()
    patient = next((p for p in patients if p["id"] == pid), None)
    if not patient:
        print("  ❌  Patient not found.")
        pause(); return

    print(f"\n  Patient: {patient['name']}  ({patient['blood_group']})\n")
    print(f"  {'ID':<8} {'Name':<22} {'Specialization':<20} {'Available'}")
    line()
    for d in doctors:
        print(f"  {d['id']:<8} {d['name']:<22} {d['specialization']:<20} {d['available_days']}")
    line()

    did    = input("  Doctor ID          : ").strip()
    doctor = next((d for d in doctors if d["id"] == did), None)
    if not doctor:
        print("  ❌  Doctor not found.")
        pause(); return

    date   = input("  Date (YYYY-MM-DD)  : ").strip() or today()
    time   = input("  Time (e.g. 10:00 AM): ").strip()
    reason = input("  Reason / Symptoms  : ").strip()

    aid = gen_id("A")
    row = {
        "id": aid,
        "patient_id": pid,   "patient_name": patient["name"],
        "doctor_id": did,    "doctor_name":  doctor["name"],
        "date": date,        "time": time,
        "reason": reason,    "status": "Scheduled"
    }
    append_csv(APPOINTMENTS_FILE, A_FIELDS, row)
    print(f"\n  ✅  Appointment booked!  ID: {aid}")
    print(f"  📋  {patient['name']}  →  {doctor['name']}  on {date} at {time}")
    pause()


def view_appointments():
    header("All Appointments")
    rows = read_csv(APPOINTMENTS_FILE)
    if not rows:
        print("  No appointments found.")
        pause(); return
    print(f"\n  {'ID':<8} {'Patient':<20} {'Doctor':<22} {'Date':<12} {'Time':<12} {'Status'}")
    line()
    for r in rows:
        status_icon = "✅" if r["status"] == "Scheduled" else "❌"
        print(f"  {r['id']:<8} {r['patient_name']:<20} {r['doctor_name']:<22} "
              f"{r['date']:<12} {r['time']:<12} {status_icon} {r['status']}")
    print(f"\n  Total: {len(rows)} appointment(s)")
    pause()


def cancel_appointment():
    header("Cancel Appointment")
    aid  = input("  Enter Appointment ID: ").strip()
    rows = read_csv(APPOINTMENTS_FILE)
    found = False
    for r in rows:
        if r["id"] == aid:
            r["status"] = "Cancelled"
            found = True
    if found:
        write_csv(APPOINTMENTS_FILE, A_FIELDS, rows)
        print("  ✅  Appointment cancelled.")
    else:
        print("  ❌  Appointment ID not found.")
    pause()


def search_appointments_by_patient():
    header("Search Appointments by Patient")
    pid  = input("  Enter Patient ID: ").strip()
    rows = read_csv(APPOINTMENTS_FILE)
    hits = [r for r in rows if r["patient_id"] == pid]
    if not hits:
        print("  No appointments found for this patient.")
    else:
        print(f"\n  {'ID':<8} {'Doctor':<22} {'Date':<12} {'Time':<12} {'Status'}")
        line()
        for r in hits:
            print(f"  {r['id']:<8} {r['doctor_name']:<22} {r['date']:<12} {r['time']:<12} {r['status']}")
    pause()


# ══════════════════════════════════════════════════════════
#   ██████  BILLING MODULE
# ══════════════════════════════════════════════════════════

def generate_bill(pid=None, pname=None):
    header("Generate Patient Bill")

    if not pid:
        pid = input("  Enter Patient ID: ").strip()
        patients = read_csv(PATIENTS_FILE)
        p = next((x for x in patients if x["id"] == pid), None)
        pname = p["name"] if p else "Unknown Patient"

    # Find the most recent doctor for this patient
    appts    = read_csv(APPOINTMENTS_FILE)
    doc_name = "N/A"
    for a in reversed(appts):
        if a["patient_id"] == pid:
            doc_name = a["doctor_name"]
            break

    print(f"\n  Patient : {pname}  ({pid})")
    print(f"  Doctor  : {doc_name}")
    print("\n  Enter charges (press Enter for ₹0):\n")

    try:
        consultation = float(input("  Consultation Fee   : ₹") or 0)
        medicine     = float(input("  Medicine Charges   : ₹") or 0)
        room         = float(input("  Room / Bed Charges : ₹") or 0)
        tests        = float(input("  Lab / Test Charges : ₹") or 0)
    except ValueError:
        print("  ❌  Invalid amount entered.")
        pause(); return

    total = consultation + medicine + room + tests
    bid   = gen_id("B")

    row = {
        "bill_id": bid, "patient_id": pid, "patient_name": pname,
        "doctor_name": doc_name, "date": today(),
        "consultation": consultation, "medicine": medicine,
        "room": room, "tests": tests, "total": total
    }
    append_csv(BILLS_FILE, B_FIELDS, row)

    # Print receipt
    print()
    line("═")
    print(f"          🧾  BILL RECEIPT  —  {today()}")
    line("═")
    print(f"  Bill ID        : {bid}")
    print(f"  Patient Name   : {pname}")
    print(f"  Patient ID     : {pid}")
    print(f"  Doctor         : {doc_name}")
    line()
    print(f"  Consultation Fee   : ₹{consultation:>9.2f}")
    print(f"  Medicine Charges   : ₹{medicine:>9.2f}")
    print(f"  Room / Bed Charges : ₹{room:>9.2f}")
    print(f"  Lab / Test Charges : ₹{tests:>9.2f}")
    line()
    print(f"  TOTAL AMOUNT       : ₹{total:>9.2f}")
    line("═")
    print("       Thank you! Wishing you a speedy recovery.")
    line("═")
    pause()


def view_all_bills():
    header("All Bills")
    rows = read_csv(BILLS_FILE)
    if not rows:
        print("  No bills generated yet.")
        pause(); return
    total_rev = 0
    print(f"\n  {'Bill ID':<8} {'Patient':<20} {'Doctor':<22} {'Date':<12} {'Amount'}")
    line()
    for r in rows:
        amt = float(r["total"])
        total_rev += amt
        print(f"  {r['bill_id']:<8} {r['patient_name']:<20} {r['doctor_name']:<22} "
              f"{r['date']:<12} ₹{amt:>9,.2f}")
    line()
    print(f"  {'TOTAL REVENUE':<62} ₹{total_rev:>9,.2f}")
    line()
    print(f"\n  Total bills: {len(rows)}")
    pause()


# ══════════════════════════════════════════════════════════
#   ██████  DASHBOARD
# ══════════════════════════════════════════════════════════

def dashboard():
    clear()
    patients = read_csv(PATIENTS_FILE)
    doctors  = read_csv(DOCTORS_FILE)
    appts    = read_csv(APPOINTMENTS_FILE)
    bills    = read_csv(BILLS_FILE)

    admitted   = sum(1 for p in patients if p.get("status") == "Admitted")
    discharged = sum(1 for p in patients if p.get("status") == "Discharged")
    scheduled  = sum(1 for a in appts    if a.get("status") == "Scheduled")
    revenue    = sum(float(b["total"])   for b in bills) if bills else 0.0

    print()
    line("═")
    print("     🏥   CITYCARE HOSPITAL MANAGEMENT SYSTEM")
    line("═")
    print(f"   📅  {now()}")
    line()
    print(f"   👥  Total Patients      : {len(patients)}")
    print(f"   🛏️   Currently Admitted  : {admitted}")
    print(f"   🏠  Discharged          : {discharged}")
    print(f"   👨‍⚕️  Doctors on Staff    : {len(doctors)}")
    print(f"   📋  Scheduled Appts.    : {scheduled}")
    print(f"   💰  Total Revenue       : ₹{revenue:,.2f}")
    line("═")


# ══════════════════════════════════════════════════════════
#   ██████  SUB-MENUS
# ══════════════════════════════════════════════════════════

def patient_menu():
    while True:
        clear()
        header("Patient Management")
        print("  1.  Register New Patient")
        print("  2.  View All Patients")
        print("  3.  Search Patient")
        print("  4.  Update Patient Record")
        print("  5.  Discharge Patient")
        print("  0.  ← Back to Main Menu")
        ch = input("\n  Enter choice: ").strip()
        actions = {
            "1": register_patient,
            "2": view_all_patients,
            "3": search_patient,
            "4": update_patient,
            "5": discharge_patient,
        }
        if ch == "0":
            break
        elif ch in actions:
            actions[ch]()
        else:
            print("  ❌  Invalid option.")
            pause()


def doctor_menu():
    while True:
        clear()
        header("Doctor Management")
        print("  1.  View All Doctors")
        print("  2.  Add New Doctor")
        print("  3.  Remove Doctor")
        print("  0.  ← Back to Main Menu")
        ch = input("\n  Enter choice: ").strip()
        actions = {"1": view_doctors, "2": add_doctor, "3": remove_doctor}
        if ch == "0":
            break
        elif ch in actions:
            actions[ch]()
        else:
            print("  ❌  Invalid option.")
            pause()


def appointment_menu():
    while True:
        clear()
        header("Appointment Management")
        print("  1.  Book New Appointment")
        print("  2.  View All Appointments")
        print("  3.  Search by Patient ID")
        print("  4.  Cancel Appointment")
        print("  0.  ← Back to Main Menu")
        ch = input("\n  Enter choice: ").strip()
        actions = {
            "1": book_appointment,
            "2": view_appointments,
            "3": search_appointments_by_patient,
            "4": cancel_appointment,
        }
        if ch == "0":
            break
        elif ch in actions:
            actions[ch]()
        else:
            print("  ❌  Invalid option.")
            pause()


def billing_menu():
    while True:
        clear()
        header("Billing")
        print("  1.  Generate Bill for Patient")
        print("  2.  View All Bills & Revenue")
        print("  0.  ← Back to Main Menu")
        ch = input("\n  Enter choice: ").strip()
        actions = {"1": generate_bill, "2": view_all_bills}
        if ch == "0":
            break
        elif ch in actions:
            actions[ch]()
        else:
            print("  ❌  Invalid option.")
            pause()


# ══════════════════════════════════════════════════════════
#   ██████  MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════

def main():
    seed_doctors()
    while True:
        dashboard()
        print("\n  MAIN MENU")
        print("  1.  👥  Patient Management")
        print("  2.  👨‍⚕️  Doctor Management")
        print("  3.  📋  Appointment Management")
        print("  4.  🧾  Billing")
        print("  0.  🚪  Exit")
        ch = input("\n  Enter choice: ").strip()
        menus = {
            "1": patient_menu,
            "2": doctor_menu,
            "3": appointment_menu,
            "4": billing_menu,
        }
        if ch == "0":
            clear()
            print("\n  👋  Thank you for using CityCare HMS. Goodbye!\n")
            break
        elif ch in menus:
            menus[ch]()
        else:
            print("  ❌  Invalid option.")
            pause()


if __name__ == "__main__":
    main()
