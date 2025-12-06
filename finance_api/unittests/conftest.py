###########################################################################
#     love; not wrong (brave) - EDEN
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-07
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

import pytest # pyright: ignore[reportMissingImports]
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from finance_api.app.main import app
from finance_api.app.database import Base, get_db

###########################################################################
#
#   region Helpers
#
###########################################################################

###########################################################################
#
#   region Program Specific Globals
#
###########################################################################

#   setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={ "check_same_thread": False }
)
TestingSessionLocal = sessionmaker( autocommit=False, autoflush=False, bind=engine )

###########################################################################
#
#   region Class Definitions
#
###########################################################################

# fixture to create a new database session for each test
@pytest.fixture( scope="function" )
def db_session():
    # create the tables in the test database
    Base.metadata.create_all( bind=engine )
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # drop the tables after tests finish to clean up
        Base.metadata.drop_all( bind=engine )

# fixture to create a TestClient that uses the test database session
@pytest.fixture( scope="function" )
def client( db_session ):
    # dependency override function
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    # apply the override
    app.dependency_overrides[ get_db ] = override_get_db
    
    # return the TestClient
    with TestClient( app ) as c:
        yield c

