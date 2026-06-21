# HOSPITAL-MANAGEMENT-SYSTEM
A python project of hospital management system 
# CityCare Hospital Management System 🏥

A Python command-line application for managing hospital operations — patients, doctors, appointments, and billing — built with plain Python and CSV file storage.

## Overview

The CityCare Hospital Management System is a command-line application that:

- Registers, searches, updates, and discharges patients
- Maintains a staff directory of doctors with specialization and availability
- Books, views, searches, and cancels patient appointments
- Generates itemized bills and tracks total hospital revenue
- Shows a live dashboard summarizing hospital activity on every run

## Features

✅ **Patient Management**: Register, view, search, update, and discharge patients
✅ **Doctor Management**: Add, view, and remove doctors with specialization and availability
✅ **Appointment Scheduling**: Book, view, search by patient, and cancel appointments
✅ **Billing System**: Generate itemized bills (consultation, medicine, room, tests) with auto-calculated totals
✅ **Live Dashboard**: Real-time counts of admitted/discharged patients, doctors, scheduled appointments, and revenue
✅ **Persistent Storage**: All data saved automatically to CSV files — no database setup required
✅ **Auto-Seeded Doctors**: 5 default doctors loaded automatically on first run
✅ **Modular Code**: Functions organized by module (patient, doctor, appointment, billing) for easy maintenance

## What You'll Learn

This project demonstrates:

- **File Handling**: Reading and writing structured data with Python's `csv` module
- **Data Structures**: Dictionaries and lists for in-memory record handling
- **String Operations**: Formatting, padding, and case handling for clean CLI output
- **Control Flow**: While loops, for loops, and if-else conditionals driving menu navigation
- **Functions**: Modular design with single-responsibility functions per feature
- **State Management**: Tracking patient status, appointment status, and running totals across a session
- **ID Generation**: Randomized unique ID creation for patients, doctors, appointments, and bills

## Project Structure

```
hospital-management-system/
├── main.py                    # Main application code
├── test_cases.txt            # Manual test cases with expected outputs
├── README.md                 # This file
├── .gitignore                 # Ignores generated CSV data files
└── REPORT.docx                # Project report (add your own)
```

## Installation

### Requirements

- Python 3.7 or higher

