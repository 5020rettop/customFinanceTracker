###########################################################################
#     Gravity - EDEN
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-07
###########################################################################

###########################################################################
#
#   region Imports
#
###########################################################################

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

def test_create_category_and_transaction( client ):
    # create a Category
    # We send a POST request to /categories/
    response = client.post(
        "/categories/",
        json={"name": "Groceries"}
    )
    assert response.status_code == 200 # OK
    category_id = response.json()[ "id" ]
    assert response.json()[ "name" ] == "Groceries"

    # create a Transaction linked to that Category
    response = client.post(
        "/transactions/",
        json={
            "amount": 50.0,
            "description": "Apples",
            "date": "2023-10-31",
            "type": "expense",
            "category_id": category_id
        }
    )
    assert response.status_code == 200 # OK
    data = response.json()
    assert data[ "amount" ] == 50.0
    assert data[ "description" ] == "Apples"
    assert data[ "category" ][ "id" ] == category_id

def test_read_transactions( client ):
    # First, setup data (create a category and transaction)
    client.post( "/categories/", json={ "name": "Rent" } )
    # Get the category we just made (we know it's ID 1 because the DB resets)
    client.post(
        "/transactions/",
        json={
            "amount": 1000.0,
            "description": "November Rent",
            "date": "2023-11-01",
            "type": "expense",
            "category_id": 1
        }
    )

    # test reading the list
    response = client.get( "/transactions/" )
    assert response.status_code == 200 # OK
    data = response.json()
    assert len(data) == 1
    assert data[0][ "description" ] == "November Rent"