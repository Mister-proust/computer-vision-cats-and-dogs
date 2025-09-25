from sqlalchemy import create_engine, Column, Integer, Float, Boolean, DateTime, text, String, ForeignKey, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  

engine = create_engine(DATABASE_URL)
connected = False
while not connected:
    try:
        conn = engine.connect()
        conn.close()
        connected = True
    except Exception:
        print("Attente de PostgreSQL...")
        time.sleep(2)
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

    feedbacks = relationship("FeedbackUsers", back_populates="time_metric")

class FeedbackUsers(Base):
    __tablename__ = "feedback_users"
    __table_args__ = {"schema": "monitoring"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(String, nullable=False)  
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    feedback = Column(Integer, nullable=False)  
    prediction = Column(String, nullable=False) 

    time_metric_id = Column(Integer, ForeignKey("monitoring.time_metrics.id"), nullable= True)
    timestamp = Column(DateTime, default = datetime.utcnow)
    time_metric = relationship("time_metrics", back_populates="feedbacks")


Base.metadata.create_all(bind=engine)