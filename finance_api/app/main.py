###########################################################################
#     Un p'tit voyage - Greg Gontier
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-01
###########################################################################

# Setup:
#      1. Activate virtual environment: cd venv/Scripts/; activate.bat
#      2.Run server: uvicorn finance_api.app.main:app --reload

###########################################################################
#
#   region Standard Imports
#
###########################################################################

from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

###########################################################################
#
#   region Local Imports
#
###########################################################################

from .database import engine, SessionLocal
from . import models
from .routers import categories, transactions, auth

###########################################################################
#
#   region Helpers
#
###########################################################################

def test_insert_transaction( 
        amount : float,
        desc : str,
        _date : date,
        type : str,
        category_id : int
):
    # create db session
    db = SessionLocal()

    # new transaction
    new_transaction = models.Transaction(
        amount=amount,
        description=desc,
        date=_date,
        type=type,
        category_id=category_id
    )

    # Add and commit the transaction
    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        print(f"Transaction inserted successfully with ID: {new_transaction.id}")
    except Exception as e:
        db.rollback()
        print(f"Error inserting transaction: {e}")
    finally:
        db.close()
        
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

# configure CORS
origins = [
    "http://localhost:5173", # react app url
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # allow all methods (POST, GET, etc.)
    allow_headers=["*"],
)

# include routers
app.include_router( auth.router )
app.include_router( categories.router )
app.include_router( transactions.router )

@app.get( "/" )
def root():
    test_insert_transaction( amount=250.0, 
                            desc="Test via API",
                            _date=date.today(), 
                            type="income", 
                            category_id=1 
                        )
    return { "message": f'Hello {models.Transaction}' }
