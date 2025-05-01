# Developer: Devansh Barve
# Date: 2025-4-30
class InMemoryDB:
    def __init__(self):
        # main DB storage: dictionary to store key-value pairs
        self.db = {}
        # Transaction storage
        self.transaction_db = None
        self.transaction_in_progress = False
    
    def get(self, key):
        return self.db.get(key, None)
    
    def put(self, key, val):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress. Call begin_transaction() first.")
        self.transaction_db[key] = val
    
    def begin_transaction(self):
        if self.transaction_in_progress:
            raise Exception("Transaction already in progress. Commit or rollback first.")

        self.transaction_db = {}
        self.transaction_in_progress = True
    
    def commit(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress. Call begin_transaction() first.")
        
        # update database with transaction changes
        for key, value in self.transaction_db.items():
            self.db[key] = value
        # clear transaction storage
        self.transaction_db = None
        self.transaction_in_progress = False
    
    def rollback(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress. Call begin_transaction() first.")
        
        # clear transaction storage without applying changes to the main DB
        self.transaction_db = None
        self.transaction_in_progress = False


def sample_tests():
    # You can add more tests or modify the existing ones as needed
    # These are basic tests from the Fig. 2 in the assignment description

    print("Sample tests for InMemoryDB")
    inmemoryDB = InMemoryDB()
    
    # should return null, because A doesn’t exist in the DB yet
    result = inmemoryDB.get("A")
    print(f"Test 1: get('A') without existing key = {result}")
    assert result is None
    
    # should throw an error because a transaction is not in progress
    try:
        inmemoryDB.put("A", 5)
        print("Test 2: FAILED - put() without transaction should throw an error")
    except Exception as e:
        print(f"Test 2: PASSED - {str(e)}")
    
    # starts new transaction
    inmemoryDB.begin_transaction()
    # sets value of A to 5 but not committed yet
    inmemoryDB.put("A", 5)
    # should return null, because A is not committed yet
    result = inmemoryDB.get("A")
    print(f"Test 3: get('A') after put in transaction before commit = {result}")
    assert result is None
    
    # update A's value to 6 in transaction    
    inmemoryDB.put("A", 6)
    inmemoryDB.commit()
    result = inmemoryDB.get("A")
    print(f"Test 4: get('A') after commit = {result}")
    assert result == 6
    
    #  throws an error, because there is no open transaction
    try:
        inmemoryDB.commit()
        print("Test 5: FAILED - commit() without transaction.")
    except Exception as e:
        print(f"Test 5: PASSED - {str(e)}")
    
    # throws an error because there is no ongoing transaction
    try:
        inmemoryDB.rollback()
        print("Test 6: FAILED - rollback() no ongoing transaction.")
    except Exception as e:
        print(f"Test 6: PASSED - {str(e)}")
    
    # should return null because B does not exist in the database
    result = inmemoryDB.get("B")
    print(f"Test 7: get('B') non-existent key = {result}")
    assert result is None
    
    # starts a new transaction
    inmemoryDB.begin_transaction()
    # Set key B's valye to 10 within the transaction
    inmemoryDB.put("B", 10)
    # Rollback the transaction - revert any changes made to B
    inmemoryDB.rollback()
    # Should return null because changes to B were rolled back
    result = inmemoryDB.get("B")
    print(f"Test 8: begin_transcation(), put('B', 10), rollback(), then get('B') after rollback = {result}")
    assert result is None
    
    print("All tests completed.")

if __name__ == "__main__":
    # Run the sample tests to check the functionality of the InMemoryDB class   
    sample_tests()
