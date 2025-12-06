###########################################################################
#     Block me out - Gracie Abrams
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
    prefix="/categories",
    tags=["categories"]
)

###########################################################################
#
#   region Class Definitions
#
###########################################################################

@router.post( "/", response_model=schemas.Category )
def createCategory( category: schemas.CategoryCreate, db: Session = Depends( get_db ) ):
    db_category = crud.CategoryCRUD.getCategoryByName( db, name=category.name )
    if db_category:
        raise HTTPException( status_code=400, detail="Category already exists" )
    return crud.CategoryCRUD.createCategory( db=db, category=category )

@router.get( "/", response_model=List[schemas.Category] )
def readCategories( skip: int = 0, limit: int = 100, db: Session = Depends( get_db ) ):
    categories = crud.CategoryCRUD.getCategories( db, skip=skip, limit=limit )
    return categories