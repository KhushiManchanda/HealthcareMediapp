# Family Healthcare App Backend 🏥

This repository contains the robust Django REST Framework backend for the Family Healthcare Mobile App. It was architected to handle complex medical workflows, real-time appointments, AI-driven triage, and advanced medical OCR processing.

## 🌟 Core Features

The backend is logically separated into highly specialized Django apps:

### 1. 🏥 Clinic & Multi-Role User Ecosystem (`users` app)
*   **Clinic System:** Built to support multiple `Clinic` instances (hospitals, private practices).
*   **Role-Based Access Control (RBAC):** Users assume distinct identities within a clinic (`admin`, `doctor`, `patient`, `guardian`) via the `ClinicUser` model.
*   **Family Hierarchy:** The `FamilyRelationship` module empowers a primary "Guardian" account holder to securely link and manage healthcare profiles for dependents (children, spouses, elderly parents).

### 2. 📋 Specialized Health Profiles (`profiles` app)
*   **Doctor Profiles:** Extended functionality to track specialized medical data: `medical_registration_no`, `specialty`, `qualifications`, `consultation_fee`, and a dynamic `availability_schedule`.
*   **Patient Profiles:** Securely stores core medical context crucial for triage:
    *   Vitals: `blood_group`, `height_cm`, `weight_kg`.
    *   History: `allergies`, `chronic_conditions` (e.g., Asthma, Hypertension), and `current_medications`.

### 3. 📅 Appointments & Smart Trackers (`scheduling` app)
*   **Unified Health Events:** A powerful tracker system managing time-based actions across three dimensions:
    *   `appointment`: Direct consultations with medical professionals.
    *   `medicine`: Configurable pill reminders utilizing `recurrence_rule`s (e.g., "Take daily at 8 AM").
    *   `measurement`: Reminders for submitting routine vitals (e.g., Blood Pressure checks).
*   **Smart Reminders:** Integrated `ReminderNotification` system capable of triggering push notifications or SMS alerts prior to events.

### 4. 🧠 Advanced AI Medical OCR (`medical_ocr` app)
*   **Document Ingestion:** Secure endpoints (`MedicalDocument`) allowing patients to upload PDFs or images of Lab Reports, Prescriptions, and Scans.
*   **Structured AI Extraction:** Replaces rigid text scraping with an LLM-powered engine. The system automatically reads uploaded blood tests and extracts precise `ExtractedMetric` objects (e.g., mapping "Hemoglobin", "14 g/dL", parsing reference ranges, and flagging abnormalities).

### 5. 🤖 AI Triage Bot & Health Assistant (`health_assistant` app)
*   **Conversational Triage:** A safe, conversational AI layer (`TriageSession`, `TriageMessage`) allowing patients to chat regarding their symptoms before seeing a doctor.
*   **Automated Clinical Handoffs:** The bot compiles the session into a concise `ClinicalSummary`—capturing the Chief Complaint, AI Differential Diagnosis, and Severity assessment (Routine vs. Urgent). This summary is automatically handed off to the Human Doctor for review prior to the consultation.

### 6. 📝 Dynamic Pre-Consultation Forms (`forms` app)
*   **Custom Questionnaires:** Allows clinics to build and assign dynamic assessment forms (`Questionnaire`, `Question`), such as Covid Screening or Initial Intake Forms.
*   **Patient Submissions:** Tracks and links completed forms (`PatientSubmission`) directly to the patient's medical file to ensure doctors have full context.

---

## 🛠️ Tech Stack & Setup

*   **Framework:** Django 6.0+
*   **Database:** PostgreSQL (configured for native vector searches necessary for the RAG engine).
*   **Environment:** Python 3.12+

### Running Locally

1.  **Activate Virtual Environment:**
    ```bash
    # Windows
    .\venv\Scripts\Activate.ps1
    # Mac/Linux
    source venv/bin/activate
    ```

2.  **Ensure PostgreSQL is running** and credentials match `backend_core/settings.py`.

3.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Create Superuser (for Admin Access):**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Start Server:**
    ```bash
    python manage.py runserver
    # Access the Admin panel at http://127.0.0.1:8000/admin
    ```
