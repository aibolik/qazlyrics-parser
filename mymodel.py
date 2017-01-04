# coding: utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import db

Base = declarative_base()
metadata = MetaData()

class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(200), nullable=True)
    img = Column(String(500), nullable=True)
    link = Column(String(500), nullable=True)
    lang = Column(String(10), nullable=True)
    songs = relationship("Song",  back_populates="artist")

    @property
    def serialize(self):
        return {
            'id'        : self.id,
            'fullname'  : self.fullname,
            'img'       : self.img,
            'link'      : self.link,
            'lang'      : self.lang
        }

class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship("Artist", back_populates="songs")
    link = Column(String(500), nullable=True)
    text = Column(String)

    @property
    def serialize(self):
        return {
            'id'        : self.id,
            'title'     : self.title,
            'artist_id' : self.artist_id,
            'link'      : self.link,
            'text'      : self.text,
            'artist'    : self.artist.fullname
        }

metadata.create_all(db.engine)
