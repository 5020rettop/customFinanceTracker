###########################################################################
#     Un p'tit voyage - Greg Gontier
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-01
###########################################################################

# Setup:
#      1. Activate virtual environment: cd venv/Scripts/; activate.bat
#      2.Run server: uvicorn app.main:app --reload

###########################################################################
#
#   region Standard Imports
#
###########################################################################

from fastapi import FastAPI

###########################################################################
#
#   region Local Imports
#
###########################################################################

from .database import engine
from . import models

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

###########################################################################
#
#   region Class Definitions
#
###########################################################################

# create db
models.Base.metadata.create_all(bind=engine)

# create app instance
app = FastAPI()

@app.get( "/" )
def root():
    return { "message": f'Hello {models.Category.id}' }