from enum import EnumType, unique
from typing import List
from sqlalchemy import Boolean, DateTime, Enum, Float, create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from jester.database.joins import AdminActivity
from sqlalchemy.orm import Session

Base = declarative_base()

@unique
class ScreenStatus(Enum):
    """Status of the applicant after initial screening"""

    PASS = 1
    """The applicant has passed initial screening"""

    FAIL = 2
    """The applicant has failed initial screening"""

@unique
class HirePhase(Enum):
    """Phase of the hiring process"""
    
    SCREEN = 1
    """Initial screening"""

    OUTREACH = 2
    """The applicant has been contacted"""

    INTERVIEW_PERSONAL = 3
    """The applicant has been invited to the first, conversational interview"""

    INTERVIEW_TECHNICAL = 4
    """The applicant has been invited to the technical interview"""

    DECISION = 5
    """Applicants have been made offers or rejected"""

    ORIENTATION = 6
    """Applicants have accepted offers and going through logistic orientation"""

    ONBOARDING = 7
    """Applicants have completed orientation and are now onboarded"""


class Applicant(Base):
    """Applicant table"""

    __tablename__ = 'applicant'
    id = Column(Integer, primary_key=True)
    role = Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    american = Column(Boolean)
    github_url = Column(String)
    linkedin_url = Column(String)
    years_experience = Column(Integer)
    ai_score = Column(Integer)
    ai_score_reasoning = Column(String)
    hopper_ratio = Column(Float)  
    active_github = Column(Boolean) 
    niches = Column(List(String))
    optionals = Column(List(String))
    heuristic_score = Column(Float)
    status = Column(EnumType(ScreenStatus))
    fail_reason = Column(String)
    resume_path = Column(String)

    hire_phase = Column(EnumType(HirePhase), default=HirePhase.SCREEN)


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

    activities = relationship(init=False, secondary=AdminActivity.__table__, back_populates="admin")

class ActivityType(Base):
    __tablename__ = 'activity_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    admins = relationship(init=False, secondary=AdminActivity.__table__, back_populates="activity_type")

class OutreachTemplate(Base):
    __tablename__ = 'outreach_message'
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    body = Column(String) 
    calendar_link = Column(String)
    hire_phase = Column(EnumType(HirePhase))

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    hiring_start = Column(DateTime)
    hiring_end = Column(DateTime)
    phase = Column(EnumType(HirePhase))


def get_engine(url='sqlite:///example.db'):
    """Create or connect to an SQLite database and return the engine."""
    engine = create_engine(url, echo=True)
    return engine

def create_database(engine):
    """Create all tables in the database."""
    Base.metadata.create_all(engine)

    # Populate database with default admin if it doesn't exist
    Session = sessionmaker(bind=engine)
    session = Session()

    if not session.query(Admin).first():
        admin = Admin(username="admin", email="")
        session.add(admin)
        session.commit()
    
    session.close()

def sqlite_session():
    # Create or connect to the database
    engine = get_engine()

    # Create tables if they don't exist
    create_database(engine)

    # Create a new session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def populate_db(session: Session):

    if not session.query(Admin).first():
        admins = [
            Admin(username="Ashia", email="livaudais@symbyai.com"),
            Admin(username="Michael", email="mjhouse@symbyai.com"),
            Admin(username="Tiffany", email="tiffanyd@symbyai.com")
        ]

        for admin in admin:
            session.add(admin)
        session.commit()


    if not session.query(ActivityType).first():
        activities = [
            ActivityType(name="Added applicant(s)", description="Manually added applicants to the pool."),
            ActivityType(name="Deleted applicant(s)", description="Manually removed applicants from the pool."),
            ActivityType(name="Sent outreach message(s)", description="Sent outreach messages to applicants."),
            ActivityType(name="Updated outreach message(s)", description="Updated the messaging used for outreach copy."),
            ActivityType(name="Added role(s)", description="Added a new role to the hiring process."),
            ActivityType(name="Updated role(s)", description="Updated the details of a role."),
            ActivityType(name="Deleted role(s)", description="Deleted a role."),
            ActivityType(name="Closed role(s)", description="Hired for a role and concluded the hiring process."),
            ActivityType(name="Updated hire phase.", description="Moved the hiring phase along for a role(s)."),
            ActivityType(name="Began orientation process.", description="Began the process of applicant's orientation"),
            ActivityType(name="Began onboarding process.", description="Began the process of applicant's onboarding")
        ]

        for activity in activities:
            session.add(activity)
        session.commit()
    
    session.close()
