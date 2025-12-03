###########################################################################
#     Kilby Girl - The Backseat Lovers
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-03
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

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

# region Category Table
class Category( Base ):
    __tablename__ = "categories"


    id = Column( Integer, primary_key=True, index=True )
    name = Column( String, unique=True, index=True )
    
    # enables categoryA.transactions and stuff ( for QoL )
    transactions = relationship( "Transaction", back_populates="category" )

# region Transaction Table
class Transaction( Base ):
    __tablename__ = "transactions"

    id = Column( Integer, primary_key=True, index=True )
    amount = Column( Float ) # money
    description = Column( String )
    date = Column( Date ) # Format: YYYY-MM-DD
    type = Column( String ) # "income", "expense", etc.
    
    # link this transaction to a category id
    category_id = Column( Integer, ForeignKey( "categories.id" ) )

    # enables transactionA.category.name and stuff ( for QoL )
    category = relationship( "Category", back_populates="transactions" )