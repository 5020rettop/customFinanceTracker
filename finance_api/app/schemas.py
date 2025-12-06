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

from pydantic import BaseModel
from datetime import date
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

#
# For Category
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

    class Config:
        # This tells Pydantic to treat SQLAlchemy models as dictionaries
        from_attributes = True 

# 
#  For Transaction
#

# base class
class TransactionBase(BaseModel):
    amount: float
    description: str
    date: date
    type: str  # "income" or "expense"

# schema for creating a transaction (user input)
class TransactionCreate(TransactionBase):
    category_id: int 

# schema for reading a transaction (API response)
class Transaction(TransactionBase):
    id: int
    category: Optional[Category] = None

    class Config:
        from_attributes = True
