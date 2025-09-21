from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path


# SQLite database in project root for simplicity
engine = create_engine(
	"sqlite:///./app.db",
	connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# Uploads directory within backend/app/uploads (resolved relative to this file)
UPLOAD_DIR = (Path(__file__).resolve().parent / "uploads").resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


