from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn

DATABASE_URL = "postgresql://postgres:wVHAaiOXOnKTdAQLRpCMBqBMFNbZjDZY@monorail.proxy.rlwy.net:27086/railway"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
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

# Pydantic schemas
class ItemCreate(BaseModel):
    title: str
    description: str
    starting_bid: float
    end_time: datetime

class BuyerCreate(BaseModel):
    name: str
    email: str

class BidCreate(BaseModel):
    item_id: int
    buyer_id: int
    amount: float

@app.get("/items")
def list_items():
    db = SessionLocal()
    items = db.query(Item).all()
    result = []
    for item in items:
        bids = db.query(Bid).filter(Bid.item_id == item.id).order_by(Bid.amount.desc()).all()
        highest_bid = bids[0].amount if bids else None
        result.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'starting_bid': item.starting_bid,
            'current_bid': item.current_bid,
            'highest_bid': highest_bid,
            'end_time': item.end_time.isoformat(),
            'time_left': (item.end_time - datetime.utcnow()).total_seconds()
        })
    db.close()
    return JSONResponse(result)

@app.post("/items", response_model=dict)
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(
        title=item.title,
        description=item.description,
        starting_bid=item.starting_bid,
        current_bid=item.starting_bid,
        end_time=item.end_time
    )
    db.add(db_item)
    db.commit()
    db.close()
    return {"message": "Item criado com sucesso!"}

@app.get("/buyers")
def get_buyers():
    db = SessionLocal()
    buyers = db.query(Buyer).all()
    result = [{'id': buyer.id, 'name': buyer.name, 'email': buyer.email} for buyer in buyers]
    db.close()
    return JSONResponse(result)

@app.post("/buyers", response_model=dict)
def create_buyer(buyer: BuyerCreate):
    db = SessionLocal()
    db_buyer = Buyer(name=buyer.name, email=buyer.email)
    db.add(db_buyer)
    db.commit()
    db.close()
    return {"message": "Comprador criado com sucesso!"}

@app.get("/bids")
def get_bids():
    db = SessionLocal()
    bids = db.query(Bid).all()
    result = [{'id': bid.id, 'amount': bid.amount, 'item_id': bid.item_id, 'buyer_id': bid.buyer_id} for bid in bids]
    db.close()
    return JSONResponse(result)

@app.post("/bids", response_model=dict)
def place_bid(bid: BidCreate):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == bid.item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item não existe")
    
    if item.end_time < datetime.utcnow():
        db.close()
        raise HTTPException(status_code=400, detail="Item já expirou")

    if bid.amount <= item.current_bid:
        db.close()
        raise HTTPException(status_code=400, detail="Lance deve ser maior que o lance atual")

    db_bid = Bid(amount=bid.amount, item_id=bid.item_id, buyer_id=bid.buyer_id)
    item.current_bid = bid.amount
    db.add(db_bid)
    db.commit()
    db.close()
    return {"message": "Lance realizado com sucesso"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Auction API",
        version="1.0.0",
        description="API for auction system",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
