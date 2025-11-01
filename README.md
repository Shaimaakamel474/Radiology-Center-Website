# 🏥 Radiology Center Management System

A complete **Radiology Center Web Application** designed to streamline workflows between **Doctors**, **Radiologists**, and **Patients**.  
Built with **Flask (Python)** for the backend and **HTML, CSS, and JavaScript** for the frontend.

---

## 🚀 Overview

This project provides an integrated web platform that connects patients, radiologists, and doctors within a radiology center.

- **Patients** can book appointments, upload personal data, and track their scan results.  
- **Radiologists** can upload scans and link them to the appropriate patient and doctor.  
- **Doctors** can review scans, write reports, and upload diagnostic results for patients to view.

---

## 🧠 System Workflow

1. **Patient**
   - Creates an account or logs in.
   - Books a scan appointment.
   - Can later view the **status and results** of their scans.

2. **Radiologist**
   - Logs in to upload **medical imaging scans** (e.g., X-rays, CT, MRI).
   - Associates uploaded scans with the correct **patient** and **doctor**.

3. **Doctor**
   - Logs in to view assigned scans.
   - Uploads diagnostic **reports** and final **results**.
   - Can review scan history for each patient.

4. **Patient**
   - Views updated scan results and doctor reports once available.

---

## 🧩 Features

| Role | Features |
|------|-----------|
| 🧑‍⚕️ **Doctor** | - View assigned patient scans<br>- Upload reports & diagnosis<br>- Manage previous cases |
| 🩻 **Radiologist** | - Upload scans for patients<br>- Assign scans to doctors<br>- Manage imaging records |
| 👩‍🦰 **Patient** | - Book appointments<br>- Track scan status<br>- View scan results and reports |

---

## 🛠️ Tech Stack

**Frontend**
- HTML5  
- CSS3  
- JavaScript  

**Backend**
- Flask (Python)

**Database**
- SQLite / MySQL (depending on setup)

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/radiology-center-system.git
   cd radiology-center-system
