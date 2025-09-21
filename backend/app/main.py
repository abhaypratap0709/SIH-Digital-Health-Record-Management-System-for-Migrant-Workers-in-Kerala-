from datetime import datetime
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db, UPLOAD_DIR
from .models import Report


app = FastAPI(title="Migrant Health Records API")


# Allow local frontend by default
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Create tables on startup (simple prototype behavior)
Base.metadata.create_all(bind=engine)


@app.get("/reports/{worker_id}")
def list_reports(worker_id: int, db: Session = Depends(get_db)):
	records = (
		db.query(Report)
		.filter(Report.worker_id == worker_id)
		.order_by(Report.date.desc())
		.all()
	)
	return [
		{
			"id": r.id,
			"date": r.date.isoformat(),
			"file": Path(r.file_path).name,
			"file_path": r.file_path,
			"hospital_id": r.hospital_id,
		}
		for r in records
	]


@app.post("/upload-report")
async def upload_report(
	worker_id: int = Form(...),
	hospital_id: int = Form(...),
	file: UploadFile = File(...),
	db: Session = Depends(get_db),
):
	if file.content_type != "application/pdf":
		raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

	# Save with a UUID prefix to avoid collisions
	safe_name = f"{uuid.uuid4().hex}_{file.filename}"
	file_location = UPLOAD_DIR / safe_name

	with file_location.open("wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

	new_report = Report(
		worker_id=worker_id,
		hospital_id=hospital_id,
		file_path=str(file_location),
		date=datetime.utcnow().date(),
	)
	db.add(new_report)
	db.commit()
	db.refresh(new_report)

	return {"message": "Report uploaded successfully", "report_id": new_report.id}


