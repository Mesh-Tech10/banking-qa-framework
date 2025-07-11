import pytest
from framework.database.db_connection import DatabaseConnection
from framework.base_test import BaseDatabaseTest

class TestTransactionDatabase(BaseDatabaseTest):
    
    def test_transaction_integrity(self):
        """Test database transaction integrity"""
        db = DatabaseConnection()
        
        # Start transaction
        initial_balance = db.get_account_balance("1234567890")
        
        # Perform transfer
        db.transfer_funds("1234567890", "0987654321", 100.00)
        
        # Verify balances
        sender_balance = db.get_account_balance("1234567890")
        receiver_balance = db.get_account_balance("0987654321")
        
        assert sender_balance == initial_balance - 100.00
        assert receiver_balance == initial_balance + 100.00
        
        # Verify audit log
        audit_logs = db.get_transaction_logs("1234567890")
        assert len(audit_logs) > 0
        assert audit_logs[-1]["amount"] == 100.00
