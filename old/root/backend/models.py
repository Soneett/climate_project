from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String)
    type = Column(String)
    parent_id = Column(Integer, ForeignKey('regions.id'))  


class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)  
    name = Column(String, nullable=False)  


class IndicatorSubtype(Base):
    __tablename__ = 'indicator_subtypes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Indicator(Base):
    __tablename__ = 'indicators'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'))  
    type = Column(String)                               
    theme = Column(String)                             
    subtype_id = Column(Integer, ForeignKey('indicator_subtypes.id'))


class DataSource(Base):
    __tablename__ = 'data_sources'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 
    url = Column(String)
    organization = Column(String)
    date_collected = Column(String)    
    notes = Column(Text)


class IndicatorValue(Base):
    __tablename__ = 'indicator_values'
    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey('indicators.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))
    year = Column(Integer, nullable=False)  
    value = Column(Float)
    source_id = Column(Integer, ForeignKey('data_sources.id'))


class PopulationAgeSex(Base):
    __tablename__ = 'population_age_sex'
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'))
    year = Column(Integer, nullable=False)
    age_code = Column(String, nullable=False) 
    sex_code = Column(String, nullable=False) 
    value = Column(Float)
    source_id = Column(Integer, ForeignKey('data_sources.id'))


class RegionalProgram(Base):
    __tablename__ = 'regional_programs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(String)        
    start_year = Column(Integer)
    end_year = Column(Integer)
    description = Column(Text)
    status = Column(String)        
    budget_total = Column(Float)   


class ProgramRegion(Base):
    __tablename__ = 'program_regions'
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('regional_programs.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'))
    date = Column(String, nullable=False)  
    type = Column(String, nullable=False)   
    severity = Column(Integer)              
    description = Column(Text)
    economic_loss = Column(Float)         