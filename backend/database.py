from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Date, Interval, ForeignKey

SQLALCHEMY_DATABASE_URL = "sqlite:///F:/WindsurfProjects/portfolio-website/data.db"

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
    login = Column(String)
    password = Column(String)

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
    skills = relationship("Skill", back_populates="resume")

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

class Skill(Base):
    __tablename__ = "skill"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    level = Column(String)
    resume_id = Column(Integer, ForeignKey("resume.id"))
    resume = relationship("Resume", back_populates="skills")

class PortfolioProjects(Base):
    __tablename__ = "portfolio_projects"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tag = Column(String)
    publish_date = Column(Date)
    text = Column(String)
    image = Column(String)

class Blog(Base):
    __tablename__ = "blog"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    tag = Column(String)
    publish_date = Column(Date)
    text = Column(String)
    image = Column(String)

try:
    Base.metadata.create_all(bind=engine)
except OperationalError:
    print("already created")
