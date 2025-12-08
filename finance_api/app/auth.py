###########################################################################
#     You're Gonna Go Far (With Brandi Carlile) - Noah Kahan, Brandi Carlile
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-07
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt # pyright: ignore[reportMissingModuleSource]
from passlib.context import CryptContext # pyright: ignore[reportMissingModuleSource]

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

# secret key for signing jwt tokens (keep this safe in real apps!)
SECRET_KEY = "super-secret-key-lol"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext( schemes=["argon2"], deprecated="auto" )

###########################################################################
#
#   region Class Definitions
#
###########################################################################

def verifyPassword( plain_password: str, hashed_password: str ) -> bool:
    return pwd_context.verify( plain_password, hashed_password )

def getPasswordHash( password: str ) -> str:
    return pwd_context.hash( password )

def createAccessToken( data: dict, expires_delta: Optional[timedelta] = None ) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now( timezone.utc ) + expires_delta
    else:
        expire = datetime.now( timezone.utc ) + timedelta( minutes=15 )

    to_encode.update( { "exp": expire } )
    encoded_jwt = jwt.encode( to_encode, SECRET_KEY, algorithm=ALGORITHM )
    return encoded_jwt