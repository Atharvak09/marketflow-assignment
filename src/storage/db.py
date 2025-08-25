from sqlalchemy import create_engine, Column, String, Float, DateTime, Text, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import json
import os

Base = declarative_base()

class ContractRow(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(32), index=True)
    market_id = Column(String(64), index=True)
    contract_id = Column(String(64), index=True)
    question = Column(Text)
    outcome = Column(String(64))
    yes_price = Column(Float)  # 0..1
    url = Column(Text)
    extra = Column(Text)
    fetched_at = Column(DateTime, default=datetime.utcnow)

def get_session(db_path: str = "./out/markets.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}", echo=False, future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)()
