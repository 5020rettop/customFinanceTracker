###########################################################################
#     Best - Gracie Abrams
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-06
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

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

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

###########################################################################
#
#   region Class Definitions
#
###########################################################################

@router.post( "/", response_model=schemas.Transaction )
def createTransaction( transaction: schemas.TransactionCreate, db: Session = Depends( get_db ) ):
    return crud.TransactionCRUD.createTransaction( db=db, transaction=transaction )

@router.get( "/", response_model=List[schemas.Transaction] )
def readTransactions( skip: int = 0, limit: int = 100, db: Session = Depends( get_db ) ):
    transactions = crud.TransactionCRUD.getTransactions( db, skip=skip, limit=limit )
    return transactions