###########################################################################
#     I miss you, I'm sorry - Gracie Abrams
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-07
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import crud, schemas, database, auth

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

router = APIRouter( tags=[ "authentication" ] )

###########################################################################
#
#   region Class Definitions
#
###########################################################################

@router.post( "/signup", response_model=schemas.User )
def createUser( user: schemas.UserCreate, 
               db: Session = Depends( database.get_db ) ):
    
    # check if user already exists
    db_user = crud.UserCRUD.getUserByEmail( db, email=user.email )
    if db_user:
        raise HTTPException( status_code=400, detail="Email already registered" )
    return crud.UserCRUD.createUser( db=db, user=user )

@router.post( "/token", response_model=schemas.Token )
def loginForAccessTokens( form_data: OAuth2PasswordRequestForm = Depends(), 
                            db: Session = Depends( database.get_db ) ):

    # check if user exists
    user = crud.UserCRUD.getUserByEmail( db, form_data.username )
    if not user:
        raise HTTPException( status_code=400, detail="Incorrect email or password" )
    
    # verify password
    if not auth.verifyPassword( form_data.password, user.hashed_password ):
        raise HTTPException( status_code=400, detail="Incorrect email or password" )
    
    # create access token
    access_token_expires = timedelta( minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES )
    access_token = auth.createAccessToken(
        data={ "sub": user.email }, expires_delta=access_token_expires
    )

    return { "access_token": access_token, "token_type": "bearer" }