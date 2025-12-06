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

from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import getCurrentUser

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
def createTransaction(
        transaction: schemas.TransactionCreate, 
        db: Session = Depends(get_db),
        current_user: models.User = Depends(getCurrentUser) ) -> schemas.Transaction:

    # Pass current_user.id to crud
    return crud.TransactionCRUD.createTransaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get( "/", response_model=List[schemas.Transaction] )
def readTransactions( 
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends( get_db ), 
        current_user: models.User = Depends(getCurrentUser) ) -> List[ schemas.Transaction ]:
    
    transactions = crud.TransactionCRUD.getTransactions( db, user_id=current_user.id, skip=skip, limit=limit )
    return transactions

@router.delete( "/{transaction_id}" )
def deleteTransaction( 
        transaction_id: int, 
        db: Session = Depends( get_db ), 
        current_user: models.User = Depends(getCurrentUser) ) -> dict:
    # check if transaction exists
    db_transaction = crud.TransactionCRUD.getTransactions( db, user_id=current_user.id )
    # iterate through transactions to find by id
    if not any( t.id == transaction_id for t in db_transaction ):
        raise HTTPException( status_code=404, detail="Transaction not found" )          
        
    # delete transaction
    crud.TransactionCRUD.deleteTransaction( db, transaction_id=transaction_id )
    return { "detail": "Transaction deleted successfully" }

@router.get( "/breakdown", response_model=List[ schemas.CategoryBreakdown ] )
def getBreakdown( db: Session = Depends( get_db ), current_user: models.User = Depends(getCurrentUser) ) -> List[ schemas.CategoryBreakdown ]:
    return crud.TransactionCRUD.getExpensesByCategory( db, user_id=current_user.id )

@router.get( "/monthly", response_model=List[ schemas.MonthlySummary ] )
def getMonthlySummary( db: Session = Depends( get_db ), current_user: models.User = Depends(getCurrentUser) ) -> List[ schemas.MonthlySummary ]:
    return crud.TransactionCRUD.getMonthlySummary( db, user_id=current_user.id )