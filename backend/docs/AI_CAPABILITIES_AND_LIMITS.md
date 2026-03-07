# 🤖 AI Capabilities & Architecture Constraints

**Date:** March 2026

When building a high-grade Healthcare MVP, we must differentiate between native backend execution, third-party API dependencies, and frontend-driven UI experiences.

## ✅ What We CAN Implement Securely Now

### 1. Smart Triage NLP Bot (`health_assistant`)
We have full capability to build an intelligent, context-aware chatbot using the **Language Model API (e.g., OpenAI/Gemini)** natively in our backend. 
* **How:** We ingest the user's EHR via a Retrieval-Augmented Generation (RAG) prompt, pass their typed/spoken symptoms to the API, and securely return a response and structured `TriageSession` object.
* **Result:** A highly intelligent "Mental Health / Triage Bot" utilizing text (or Speech-to-Text on the mobile app side).

### 2. Medical OCR Prescription Scanner (`medical_ocr`)
We are fully capable of scanning uploads using Vision models in the backend asynchronously.
* **How:** An uploaded image is placed into a background Celery task, parsed via an LLM, and JSON extracted (Medicine Name, Dosage).
* **Result:** Magic extraction of medicine data into reminders.

### 3. Human-to-Human Video Consultations (`communication`)
We are fully capable of laying the groundwork for live video telehealth.
* **How:** Generating secure WebRTC tokens or leveraging third-parties like Agora/Twilio in the backend to create secure video rooms for doctors and patients.

---

## 🚫 What We SHOULD NOT Build from Scratch (or Native Limitations)

### 1. The "Real-Time AI Video Avatar" (VideoBot)
Creating a truly real-time AI Video Avatar (where the AI visibly talks back in a 3D animated or deepfake human form) is an extreme undertaking natively. It requires generating video frames dynamically per second and establishing intense backend pipelines for ultra-low latency. 

**Startup Recommendation:** 
Instead of building a real-time deepfake avatar manually, we will implement the logic of the **Text/Voice Assistant**, which natively outputs high-quality text responses. If an actual "Animated Video Avatar" is strictly required by stakeholders/investors, we must rely entirely on specialized SaaS platforms (like **HeyGen** or **Tavus**) via their frontend SDKs. A natively built generic 3D avatar within Django is out of scope and usually results in poor UX.

### 2. Smartwatch Direct Ingestion
Watches do not hit our API directly continuously. 
**Startup Recommendation:** We will construct Webhook endpoints (`/api/health/wearables/`). The *Frontend Mobile App* reads Apple Health/Google Fit, and then POSTs these standardized metrics occasionally to our secure Django backend.
