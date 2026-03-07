# 📡 CareSync: Core API Schema & Request Payloads

This document defines the exact shape of the JSON data the Frontend needs to send (Requests) and expect back (Responses) when interacting with the Django REST Framework backend.

All endpoints require a valid JWT token in the `Authorization: Bearer <token>` header unless specified.

---

## 🔐 1. Authentication & Users

### Login (Obtain Tokens)
**Endpoint:** `POST /api/token/`
**No Auth Required**

**Request payload:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response payload:**
```json
{
  "access": "eyJhbGciOiJIUzI1Ni...",
  "refresh": "eyJhbGciOiJIUzI1Ni..."
}
```

### Create Clinic User
**Endpoint:** `POST /api/users/clinic-users/`

**Request payload:**
```json
{
  "user": "550e8400-e29b-41d4-a716-446655440000",
  "clinic": "11223344-e29b-41d4-a716-446655440000",
  "role": "patient",
  "is_active": true
}
```

---

## 📅 2. Scheduling & Telemedicine

### Book an Appointment 
*(Triggers the automated Chat Room creation signal)*
**Endpoint:** `POST /api/scheduling/book/`

**Request payload:**
```json
{
  "doctor_id": "8bb34106-a0ff-4e56-9e9b-9c987820bb12",
  "start_datetime": "2026-03-10T14:30:00Z",
  "title": "Severe back pain consultation"
}
```

**Response payload (Success):**
```json
{
  "success": true, 
  "message": "Appointment booked and Chat room bridged successfully.",
  "appointment_id": "a9101b54-9321-4d1a-81a1-f76191b223c6"
}
```

### Fetch Unified Calendar (Patient or Doctor View)
**Endpoint:** `GET /api/scheduling/unified/?start_date=2026-03-01&end_date=2026-03-31`

**Response payload:**
```json
{
  "count": 2,
  "results": [
    {
      "id": "appointment-a9101",
      "event_type": "appointment",
      "source_id": "a9101b54-9321-4d1a-81a1-f76191b223c6",
      "title": "Severe back pain consultation",
      "start_datetime": "2026-03-10T14:30:00Z",
      "end_datetime": "2026-03-10T15:00:00Z",
      "status": "scheduled",
      "color": "#3357FF",
      "doctor_name": "Dr. Sarah Adams"
    },
    {
      "id": "medicine-b8823",
      "event_type": "medicine",
      "title": "Take Ibuprofen 400mg",
      "start_datetime": "2026-03-10T20:00:00Z",
      "is_recurring": true,
      "recurrence_rule": "FREQ=DAILY;COUNT=7",
      "color": "#FF5733"
    }
  ]
}
```

---

## 💬 3. Chat & Communication

### Send Direct Message
**Endpoint:** `POST /api/communication/messages/`

**Request payload (Text Message):**
```json
{
  "conversation": "d4fe3e50-bd18-4b95-a4ab-b631d8c11e2f",
  "message_type": "text",
  "content": "Doctor, is it normal to feel drowsy after the medication?"
}
```

**Request payload (File Upload/Image):**
*(Must be sent as `multipart/form-data` instead of JSON if including an actual file)*
```json
{
  "conversation": "d4fe3e50-bd18-4b95-a4ab-b631d8c11e2f",
  "message_type": "image",
  "attachment": "(Binary File Data)"
}
```

---

## 🤖 4. AI Triage Assistant

### Send AI Chat Message
**Endpoint:** `POST /api/triage/sessions/{session_id}/message/`

**Request payload:**
```json
{
  "content": "I have been experiencing a sharp pain in my lower right abdomen for the past 6 hours, accompanied by nausea."
}
```

**Response payload:**
```json
{
  "success": true,
  "ai_response": "Based on the severe location and sudden onset combined with nausea, this may be an acute issue such as appendicitis. I am flagging this as HIGH severity and generating a clinical summary for the on-call doctor immediately."
}
```

---

## 📁 5. Medical Document Vault (OCR)

### Upload New Medical Record
**Endpoint:** `POST /api/records/documents/`
*(Send as `multipart/form-data`)*

**Request payload:**
```json
{
  "patient": "550e8400-e29b-41d4-a716-446655440000",
  "document_type": "lab_report",
  "file": "(Blood_Test_Dec.pdf)"
}
```

### Fetch Extracted Metrics (e.g. for charts)
**Endpoint:** `GET /api/records/metrics/?document={document_id}`

**Response payload:**
```json
[
  {
    "id": "111-222",
    "metric_name": "Fasting Blood Sugar",
    "value": "126",
    "unit": "mg/dL",
    "reference_range": "70-99",
    "is_abnormal": true,
    "measured_date": "2026-03-01"
  },
  {
    "id": "333-444",
    "metric_name": "Hemoglobin",
    "value": "14.2",
    "unit": "g/dL",
    "reference_range": "13.8-17.2",
    "is_abnormal": false,
    "measured_date": "2026-03-01"
  }
]
```
