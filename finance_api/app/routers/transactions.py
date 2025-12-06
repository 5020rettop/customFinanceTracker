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

@router.delete( "/{transaction_id}" )
def deleteTransaction( transaction_id: int, db: Session = Depends( get_db ) ):
    # check if transaction exists
    db_transaction = crud.TransactionCRUD.getTransactions( db )
    # iterate through transactions to find by id
    if not any( t.id == transaction_id for t in db_transaction ):
        raise HTTPException( status_code=404, detail="Transaction not found" )
        
    # delete transaction
    crud.TransactionCRUD.deleteTransaction( db, transaction_id=transaction_id )
    return { "detail": "Transaction deleted successfully" }