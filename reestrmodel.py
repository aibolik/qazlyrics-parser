# coding: utf-8
from sqlalchemy import Column, DateTime, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON
import db

Base = declarative_base()
metadata = Base.metadata

class AuctionBase(Base):
    __tablename__ = 'auction'

    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=True)
    number = Column(Integer, nullable=True)
    start_price = Column(Integer, nullable=True)
    typeof = Column(String(500), nullable=True)
    periodicity = Column(String(200), nullable=True)
    minimum = Column(Integer, nullable=True)
    garanty = Column(Integer, nullable=True)
    status = Column(String(200), nullable=True)
    start_at = Column(DateTime)
    rent_pay = Column(Integer, nullable=True)
    add_info = Column(String(5000), nullable=True)
    sell_price = Column(Integer, nullable=True)
    organ = Column(Text, nullable=True)
    obj = Column(Text, nullable=True)
    balance = Column(Text, nullable=True)
    seller = Column(Text, nullable=True)
    requisites = Column(Text, nullable=True)
    publication = Column(Text, nullable=True)
    method = Column(Text, nullable=True)
    conditions = Column(Text, nullable=True)
    for_physical = Column(Text, nullable=True)
    for_juridical = Column(Text, nullable=True)
    for_individ = Column(Text, nullable=True)
    imagePath = Column(JSON, nullable=True)
    link = Column(String(1000), nullable=True)
    parsed_at = Column(DateTime, nullable=True)
    region_id = Column(Integer, nullable=True)

Base.metadata.create_all(db.engine)