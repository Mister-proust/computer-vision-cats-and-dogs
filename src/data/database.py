from sqlalchemy import create_engine, Column, Integer, Float, Boolean, DateTime, text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os


DATABASE_URL = os.getenv("DATABASE_URL")  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS monitoring;"))
    conn.commit()

class time_metrics(Base):
    __tablename__ = "time_metrics"
    __table_args__ = {"schema": "monitoring"} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    inference_time_ms = Column(Float, nullable=False)
    success = Column(Boolean, nullable=False)


Base.metadata.create_all(bind=engine)