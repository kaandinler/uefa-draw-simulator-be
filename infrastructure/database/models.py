from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base

# Association table for many-to-many relationship between draws and teams
draw_teams = Table(
    'draw_teams',
    Base.metadata,
    Column('draw_id', Integer, ForeignKey('draws.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)


class TeamModel(Base):
    """Team database model"""
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    country = Column(String(3), nullable=False)
    pot = Column(Integer, nullable=False)
    coefficient = Column(Float, nullable=False)
    logo_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    draws = relationship('DrawModel', secondary=draw_teams, back_populates='teams')
    home_fixtures = relationship('FixtureModel', foreign_keys='FixtureModel.home_team_id', back_populates='home_team')
    away_fixtures = relationship('FixtureModel', foreign_keys='FixtureModel.away_team_id', back_populates='away_team')


class DrawModel(Base):
    """Draw database model"""
    __tablename__ = 'draws'

    id = Column(Integer, primary_key=True, index=True)
    competition = Column(String(50), nullable=False)
    season = Column(String(10), nullable=False)
    is_valid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    teams = relationship('TeamModel', secondary=draw_teams, back_populates='draws')
    fixtures = relationship('FixtureModel', back_populates='draw', cascade='all, delete-orphan')


class FixtureModel(Base):
    """Fixture database model"""
    __tablename__ = 'fixtures'

    id = Column(Integer, primary_key=True, index=True)
    draw_id = Column(Integer, ForeignKey('draws.id'), nullable=False)
    home_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    matchday = Column(Integer, nullable=True)
    scheduled_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default='scheduled')
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    draw = relationship('DrawModel', back_populates='fixtures')
    home_team = relationship('TeamModel', foreign_keys=[home_team_id], back_populates='home_fixtures')
    away_team = relationship('TeamModel', foreign_keys=[away_team_id], back_populates='away_fixtures')