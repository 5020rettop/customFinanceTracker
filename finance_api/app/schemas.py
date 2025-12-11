###########################################################################
#     Fire - Noah Kahan
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-06
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

from pydantic import BaseModel, ConfigDict
from datetime import date, time
from typing import List, Optional

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
''' Pydantic models are the way FastAPI uses to define the schemas of the 
    data that it receives (requests) and returns (responses). 

    class *tableName*Create(*tableName*Base) represent the data required to create an item. 

    class *tableName*(*tableName*Base) represents the data that is returned when the items are queried. 

    The fields that are common to *tableName*Create and *tableName* are placed in 
    *tableName*Base to avoid duplication.
'''
#
#  region Category
#

# base class
class CategoryBase(BaseModel):
    name: str

# schema for creating a category (user input)
class CategoryCreate(CategoryBase):
    pass

# schema for reading a category (API response)
class Category(CategoryBase):
    id: int
    # We will add a list of transactions here later if needed, 
    # but for now, we keep it simple to avoid infinite recursion loops.

    # This tells Pydantic to treat SQLAlchemy models as dictionaries
    model_config = ConfigDict( from_attributes=True )

# 
#   region Transaction
#

# base class
class TransactionBase(BaseModel):
    amount: float
    description: str
    date: date
    time: time
    type: str  # "income" or "expense"

# schema for creating a transaction (user input)
class TransactionCreate(TransactionBase):
    category_id: int 

# schema for reading a transaction (API response)
class Transaction(TransactionBase):
    id: int
    category: Optional[Category] = None

    # This tells Pydantic to treat SQLAlchemy models as dictionaries
    model_config = ConfigDict( from_attributes=True )

#
#   region Analytics
#

class CategoryBreakdown(BaseModel):
    category: str
    total: float

class MonthlySummary(BaseModel):
    month: str
    type: str
    total: float

#
#   region Users
#

class UserBase( BaseModel ):
    email : str

class UserCreate( UserBase ):
    password : str

class User( UserBase ):
    id : int

    model_config = ConfigDict( from_attributes=True )

class Token( BaseModel ):
    access_token : str
    token_type : str

class TokenData( BaseModel ):  
    email : Optional[str] = None