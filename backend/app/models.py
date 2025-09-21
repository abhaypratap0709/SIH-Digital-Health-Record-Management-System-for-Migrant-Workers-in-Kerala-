from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	email = Column(String, unique=True, index=True, nullable=False)
	password_hash = Column(String, nullable=False)
	role = Column(String, nullable=False)  # worker/hospital/gov
	phid = Column(String, unique=True, index=True)


class Hospital(Base):
	__tablename__ = "hospitals"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	location = Column(String, nullable=True)
	created_at = Column(String, nullable=True)


class Report(Base):
	__tablename__ = "reports"

	id = Column(Integer, primary_key=True, index=True)
	worker_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
	hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False, index=True)
	file_path = Column(String, nullable=False)
	date = Column(Date, nullable=False)


class Consent(Base):
	__tablename__ = "consent"

	id = Column(Integer, primary_key=True, index=True)
	worker_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
	gov_request = Column(Boolean, nullable=False)
	status = Column(String, nullable=False)  # approved/denied/pending


