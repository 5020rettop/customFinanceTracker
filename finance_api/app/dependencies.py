###########################################################################
#     Still - Noah Kahan
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-07
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import crud, models, schemas, database, auth

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

# This tells FastAPI that the client should send the token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

###########################################################################
#
#   region Class Definitions
#
###########################################################################

def getCurrentUser( 
        token: str = Depends( oauth2_scheme ), 
        db: Session = Depends( database.get_db ) 
    ) -> models.User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode token
        payload = jwt.decode( token, auth.SECRET_KEY, algorithms=[ auth.ALGORITHM ] )
        email: str = payload.get( "sub" )
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # check if user exists
    user = crud.get_user_by_email( db, email=email )
    if user is None:
        raise credentials_exception
    return user