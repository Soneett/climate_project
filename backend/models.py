from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    type = Column(String)

class Year(Base):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)

class IndicatorType(Base):
    __tablename__ = 'indicator_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

class Indicator(Base):
    __tablename__ = 'indicators'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('indicator_types.id'))
    name = Column(String)
    unit = Column(String)
    description = Column(String)

class DataSource(Base):
    __tablename__ = 'data_sources'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    organization = Column(String)
    date_collected = Column(String)
    notes = Column(String)

class IndicatorValue(Base):
    __tablename__ = 'indicator_values'
    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey('indicators.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))
    year_id = Column(Integer, ForeignKey('years.id'))
    value = Column(Float)
    source_id = Column(Integer, ForeignKey('data_sources.id'))
