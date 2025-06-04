from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()

class PDFManager(Base):
    __tablename__ = "pdf_manager"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, nullable=False)
    original_image_link = Column(String, nullable=False)
    redacted_image_link = Column(String, nullable=True)
    llm_response = Column(Text, nullable=True)
    input_token_count = Column(Integer, nullable=True)
    output_token_count = Column(Integer, nullable=True)
    latency = Column(Float, nullable=True)
    status = Column(String, nullable=True, default="pending")   
    created_at = Column(DateTime, nullable=False, default=datetime.now)
