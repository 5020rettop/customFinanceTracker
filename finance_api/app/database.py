#!/usr/bin/env python3
###########################################################################
#     Yellow - Coldplay (Wisp Cover)
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-03
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

###########################################################################
#
#   region Helpers
#
###########################################################################

# Dependency for API requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###########################################################################
#
#   region Program Specific Globals
#
###########################################################################

# SQLite db url
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"

###########################################################################
#
#   region Class Definitions
#
###########################################################################

# Create engine
# "check_same_thread": False is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session 
# Each instance of this class will be a database session
SessionLocal = sessionmaker( autocommit=False, autoflush=False, bind=engine )

# Create a Base class
# This is the base class for all the database tables
Base = declarative_base()

