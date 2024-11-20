from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Date

SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#создаем базовый класс для моделей
class Base(DeclarativeBase): pass

class Person(Base):
    __tablename__ = "people"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    profession = Column(String)
    location = Column(String)
    email = Column(String)
    phone = Column(String)
    birth_date = Column(Date)

class About(Base):
    __tablename__ = "about"
 
    id = Column(Integer, primary_key=True, index=True)
    about_me = Column(String)
    works_on_title = Column(String)
    works_on_description = Column(String)
    works_on_icon = Column(String)
    recomendations_name = Column(String)
    recomendations_description = Column(String)
    recomendations_icon = Column(String)

class Clients(Base):
    __tablename__ = "clients"
 
    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String)
    link = Column(String)

class Resume(Base):
    __tablename__ = "resume"
 
    id = Column(Integer, primary_key=True, index=True)
    educations = relationship("Education", back_populates="resume")
    experiences = relationship("Experience", back_populates="resume")

class Education(Base):
    __tablename__ = "education"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    interval = Column(Interval)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    resume = relationship("Resume", back_populates="educations")

class Experience(Base):
    __tablename__ = "experience"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    interval = Column(Interval)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    resume = relationship("Resume", back_populates="experiences")

try:
    Base.metadata.create_all(bind=engine)
except OperationalError:
    print("already created")
