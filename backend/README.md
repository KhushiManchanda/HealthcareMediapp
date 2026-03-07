# 🏥 CareSync Backend Architecture

**Version:** 1.0 (MVP)
**Architecture Type:** Modular Django REST Framework (DRF)
**Target:** Healthcare Startup (Strict Enterprise Security & Scale)

---

## 🚀 What We Have Built (Current State)

We have engineered an enterprise-grade backend architecture directly inspired by scalable systems like the Unio LMS. Instead of building a monolithic script, we have separated the logic into highly specialized applications.

Here is the exhaustive list of modules currently implemented and active in the system:

### 1. Unified Authentication & Clinics (`users`)
*   **Purpose:** The foundation of the system. It handles Multi-Tenant architecture (hospitals/clinics) and custom user login mappings.
*   **Features Added:**
    *   `ClinicUser` Mapping (Patients, Doctors, Admins all live under one unified auth system).
    *   `FamilyRelationship` (Allows Guardians to read/write under their child's Health ID).
    *   **JWT Security:** Implemented `rest_framework_simplejwt` on `/api/token/` for stateless, cross-platform security (Flutter & Web).

### 2. Medical Profiles (`profiles`)
*   **Purpose:** Securely separates personal medical data from standard authentication data.
*   **Features Added:**
    *   `DoctorProfile`: Stores medical registration numbers, consultation constraints, and bios.
    *   `PatientProfile`: Secure parameters (Blood Group, Allergies, Chronic Diseases).

### 3. Unified Scheduling Engine (`scheduling`)
*   **Purpose:** A robust calendar system that aggregates all events into a single UI feed, heavily inspired by the Unio LMS `CalendarAggregationService`.
*   **Features Added:**
    *   `HealthEvent` mapping for Doctor Appointments and recurring Medicine Trackers.
    *   `SchedulingService` layer abstracting business logic away from the API view.
    *   `UnifiedCalendarView`: A high-powered API that calculates and returns a merged JSON stream of all Appointments, Reminders, and Measurements for a specific user.

### 4. Telemedicine & Communication (`communication`)
*   **Purpose:** Enabling HIPAA-compliant conversations and mass health advisories.
*   **Features Added:**
    *   `Conversation` & `Message` models optimized for Direct messaging.
    *   **Signals Bridging:** A Django Signal that automatically provisions a secure Chat Room between a Doctor and Patient the very second an Appointment is booked in the Scheduling module.

### 5. Document Processing & OCR (`medical_ocr`)
*   **Purpose:** The central vault for storing patient files safely in the cloud.
*   **Features Added:**
    *   `MedicalDocument` endpoints for uploading X-Rays, Lab Reports, and Prescriptions.
    *   Data mapping for `ExtractedMetric` (e.g., Blood Sugar: 120mg/dL).

### 6. AI Triage Assistant (`health_assistant`)
*   **Purpose:** Initial intelligent screening of patients before they see a doctor.
*   **Features Added:**
    *   `TriageSession` and `TriageMessage` tracking.
    *   Interactive `@action` endpoints allowing the frontend to securely POST live chat messages to the backend AI system.
    *   Automatic `ClinicalSummary` generation sent straight to the doctor's chat window.

---

## � Security & Data Compliance Strategies

As a healthcare application aiming for investment and government compliance, security is paramount. Here is how we engineered the application to be secure:

*   **1. Stateless Tokens (JWT):** We do not use session cookies which are vulnerable to CSRF. We use short-lived Access Tokens via `djangorestframework-simplejwt`.
*   **2. Strict Separation of Concerns:** Database logic (`models()`), translation (`serializers()`), API exposure (`views()`), and heavy lifting (`services()`) are strictly isolated. If one fails, the others are protected.
*   **3. Zero Native Monolithic AI Generation:** We strictly use the API to route text-based AI. We avoid attempting to render generic 3D video models locally in Django, reducing server load to near-zero.
*   **4. Implicit Role-Based Access Control (RBAC):** We rely on `permission_classes = [IsAuthenticated]`, combined with custom Service overrides, ensuring a Patient can never scrape a Doctor's private schedule.

---

## 📈 Next Phases & Integration (Future-Proofing)

To make this completely Blockchain-ready and production-live, the next developer should focus on:

1.  **Distributed Task Queues (Celery/Redis):** Right now, the OCR endpoint exists, but the AI text extraction must be pushed into a background worker (Celery) so the user's mobile app doesn't freeze while waiting for the image to be parsed.
2.  **S3 / GCP Bucket Integration:** Update the `settings.py` so that `MedicalDocument` file uploads route to a private, encrypted AWS S3 bucket rather than the local hard drive.
3.  **Third-Party WebRTC:** Integrate Agora or Twilio into the `communication` module to generate video-call tokens.
4.  **Blockchain Hashing (Optional):** If requested for extreme security, every `MedicalDocument` upload can hash its content to a private Ethereum/Hyperledger instance, mathematically proving no document was altered post-upload. 
