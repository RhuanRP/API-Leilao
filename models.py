from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:wVHAaiOXOnKTdAQLRpCMBqBMFNbZjDZY@monorail.proxy.rlwy.net:27086/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    starting_bid = Column(Float, nullable=False)
    current_bid = Column(Float, nullable=True)
    end_time = Column(DateTime, nullable=False)
    bids = relationship('Bid', backref='item', lazy=True)

class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    bids = relationship('Bid', backref='buyer', lazy=True)

class Bid(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    bid_time = Column(DateTime, default=datetime.utcnow)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=False)

Base.metadata.create_all(bind=engine)
