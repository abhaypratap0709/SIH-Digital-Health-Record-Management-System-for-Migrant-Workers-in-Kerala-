PRD.md – Migrant Health Records Prototype
🎯 Objective

Build a working prototype for SIH that demonstrates how migrant workers’ health records can be digitized, shared, and consent-controlled between hospitals and government.

This prototype must:

Be simple enough to build/debug solo in limited time.

Include a real database (SQLite) for credibility.

Run locally with minimal setup (FastAPI backend + Next.js frontend).

Showcase end-to-end flow with QR-based worker ID and consent.

👥 Users & Roles

Worker

Registers & gets Public Health ID (PHID) + QR code.

Can view prescriptions/reports.

Can approve/deny government consent requests.

Hospital Admin

Logs in.

Uploads prescription/report by scanning PHID (or typing ID).

Manages reports linked to workers.

Government Admin

Manages hospital registry.

Views analytics (total hospitals, total workers).

Requests consent from workers for data sharing.

🗄️ Database Schema (SQLite)

Tables:

users

id | name | email | password_hash | role (worker/hospital/gov) | phid


hospitals

id | name | location | created_at


reports

id | worker_id | hospital_id | file_path | date


consent

id | worker_id | gov_request (bool) | status (approved/denied/pending)

🔗 System Flow

Worker signs up → entry in users → PHID auto-generated → QR returned.

Hospital scans PHID → uploads report → entry in reports.

Worker dashboard fetches /reports?worker_id=… and shows files.

Worker toggles consent → updates consent table.

Gov dashboard fetches /analytics (counts from DB) + consent status.

🖥️ Tech Stack

Backend: FastAPI + SQLite + SQLAlchemy (simple REST API).

Frontend: Next.js + Tailwind + shadcn/ui (clean UI).

QR Code: qrcode Python lib for backend or qrcode.react for frontend.

File Storage: /uploads folder (local only).

🛠️ API Endpoints

POST /register → create user (worker/hospital/gov), return PHID+QR if worker.

POST /login → basic email/password login (JWT optional).

POST /upload-report → hospital uploads PDF, stored in /uploads, DB updated.

GET /reports/{worker_id} → worker fetches list of reports.

POST /consent → worker updates consent flag.

GET /analytics → return counts (workers, hospitals, reports).