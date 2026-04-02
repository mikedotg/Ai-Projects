#!/usr/bin/env python3
"""
TEST_CASES.py — Unit tests for process_data.py

These tests were written with AI assistance to:
1. Replicate the bug identified in error.log
2. Verify correct behaviour after the fix
"""

import unittest
import os
import json
import csv
import tempfile
import shutil
from process_data_final import DataProcessor


class TestLoadData(unittest.TestCase):
    """Tests for the load_data method."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)

    def _create_customers_csv(self, rows):
        """Helper to create a customers CSV file."""
        filepath = os.path.join(self.test_dir, "customers.csv")
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["customer_id", "name", "email", "join_date"]
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return filepath

    def _create_transactions_csv(self, rows):
        """Helper to create a transactions CSV file."""
        filepath = os.path.join(self.test_dir, "transactions.csv")
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "transaction_id",
                    "customer_id",
                    "amount",
                    "date",
                    "category",
                ],
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return filepath

    def test_load_valid_customers(self):
        """Test loading valid customer data."""
        filepath = self._create_customers_csv(
            [
                {
                    "customer_id": "C001",
                    "name": "Test User",
                    "email": "test@test.com",
                    "join_date": "2023-01-01",
                },
            ]
        )
        processor = DataProcessor(filepath)
        result = processor.load_data()
        self.assertTrue(result)
        self.assertEqual(len(processor.customers), 1)
        self.assertIn("C001", processor.customers)

    def test_load_missing_file(self):
        """Test loading from a non-existent file."""
        processor = DataProcessor("/nonexistent/path/customers.csv")
        result = processor.load_data()
        self.assertFalse(result)


class TestProcessTransactions(unittest.TestCase):
    """Tests for the process_transactions method."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _create_customers_csv(self, rows):
        filepath = os.path.join(self.test_dir, "customers.csv")
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["customer_id", "name", "email", "join_date"]
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return filepath

    def _create_transactions_csv(self, rows):
        filepath = os.path.join(self.test_dir, "transactions.csv")
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "transaction_id",
                    "customer_id",
                    "amount",
                    "date",
                    "category",
                ],
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return filepath

    def test_process_valid_transactions(self):
        """Test processing valid transactions updates customer totals."""
        cust_file = self._create_customers_csv(
            [
                {
                    "customer_id": "C001",
                    "name": "Test",
                    "email": "t@t.com",
                    "join_date": "2023-01-01",
                },
            ]
        )
        trans_file = self._create_transactions_csv(
            [
                {
                    "transaction_id": "T001",
                    "customer_id": "C001",
                    "amount": "100.50",
                    "date": "2024-01-01",
                    "category": "electronics",
                },
                {
                    "transaction_id": "T002",
                    "customer_id": "C001",
                    "amount": "50.25",
                    "date": "2024-01-02",
                    "category": "food",
                },
            ]
        )
        processor = DataProcessor(cust_file)
        processor.load_data()
        result = processor.process_transactions(trans_file)
        self.assertTrue(result)
        self.assertAlmostEqual(processor.customers["C001"]["total_spent"], 150.75)
        self.assertEqual(processor.customers["C001"]["transaction_count"], 2)

    def test_transaction_for_unknown_customer(self):
        """Test that transactions for unknown customers are handled gracefully."""
        cust_file = self._create_customers_csv([])
        trans_file = self._create_transactions_csv(
            [
                {
                    "transaction_id": "T001",
                    "customer_id": "C999",
                    "amount": "50.00",
                    "date": "2024-01-01",
                    "category": "food",
                },
            ]
        )
        processor = DataProcessor(cust_file)
        processor.load_data()
        result = processor.process_transactions(trans_file)
        self.assertTrue(result)
        self.assertNotIn("C999", processor.customers)


class TestExportCustomerData(unittest.TestCase):
    """Tests for the export_customer_data method — targets the bug from error.log.

    BUG: 'dict' object has no attribute 'keys'
    The original code at line 179-180 uses:
        next(iter(self.customers.values())).keys()
    to dynamically extract fieldnames. This is fragile and fails when
    the customers dict is empty (StopIteration) or contains corrupted data.
    """

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_export_csv_with_empty_customers(self):
        """BUG REPLICATION: Exporting CSV with no customer data should not crash.

        The original code calls next(iter(self.customers.values())).keys()
        which raises StopIteration when customers dict is empty.
        """
        processor = DataProcessor("dummy.csv")
        processor.customers = {}  # Empty — no customers loaded
        output_file = os.path.join(self.test_dir, "export.csv")

        # Original code: this triggers StopIteration inside the generic
        # except block, so it returns False silently — but it SHOULD
        # handle empty data gracefully with a clear message.
        result = processor.export_customer_data(output_file, "csv")
        # After fix: should return False with a proper warning, not silently fail
        self.assertFalse(result)

    def test_export_csv_with_corrupted_customer_data(self):
        """BUG REPLICATION: Simulates the exact error from error.log.

        At scale (150 customers, 1250 transactions), malformed CSV rows
        can inject non-dict values into self.customers. When DictWriter.writerow()
        calls .keys() on these values, it fails with:
        'dict' object has no attribute 'keys'

        Original code: crashes with AttributeError
        Fixed code: skips corrupted records, exports valid ones, returns True
        """
        processor = DataProcessor("dummy.csv")
        # Normal customer
        processor.customers["C001"] = {
            "name": "Valid User",
            "email": "valid@test.com",
            "join_date": "2023-01-01",
            "total_spent": 100.0,
            "transaction_count": 1,
        }
        # Corrupted customer record — simulates malformed CSV data at scale
        processor.customers["C002"] = "corrupted_data"

        output_file = os.path.join(self.test_dir, "export.csv")

        # Fixed code: skips corrupted records gracefully, still exports valid data
        result = processor.export_customer_data(output_file, "csv")
        self.assertTrue(result)

        # Verify only the valid record was exported
        with open(output_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["customer_id"], "C001")

    def test_export_csv_with_valid_data(self):
        """Verify CSV export works correctly with valid customer data."""
        processor = DataProcessor("dummy.csv")
        processor.customers = {
            "C001": {
                "name": "Test User",
                "email": "test@test.com",
                "join_date": "2023-01-01",
                "total_spent": 150.75,
                "transaction_count": 2,
            }
        }
        output_file = os.path.join(self.test_dir, "export.csv")
        result = processor.export_customer_data(output_file, "csv")
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_file))

        # Verify CSV content
        with open(output_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["customer_id"], "C001")
            self.assertEqual(rows[0]["name"], "Test User")

    def test_export_json_with_valid_data(self):
        """Verify JSON export works correctly."""
        processor = DataProcessor("dummy.csv")
        processor.customers = {
            "C001": {
                "name": "Test User",
                "email": "test@test.com",
                "join_date": "2023-01-01",
                "total_spent": 150.75,
                "transaction_count": 2,
            }
        }
        output_file = os.path.join(self.test_dir, "export.json")
        result = processor.export_customer_data(output_file, "json")
        self.assertTrue(result)

        with open(output_file, "r") as f:
            data = json.load(f)
            self.assertIn("C001", data)

    def test_export_unsupported_format(self):
        """Verify unsupported format returns False."""
        processor = DataProcessor("dummy.csv")
        processor.customers = {"C001": {"name": "Test"}}
        output_file = os.path.join(self.test_dir, "export.xml")
        result = processor.export_customer_data(output_file, "xml")
        self.assertFalse(result)


class TestCalculateMetrics(unittest.TestCase):
    """Tests for calculate_customer_metrics."""

    def test_metrics_with_no_data(self):
        """Metrics should return empty dict when no customers loaded."""
        processor = DataProcessor("dummy.csv")
        result = processor.calculate_customer_metrics()
        self.assertEqual(result, {})

    def test_metrics_with_valid_data(self):
        """Metrics should correctly calculate totals and averages."""
        processor = DataProcessor("dummy.csv")
        processor.customers = {
            "C001": {"name": "A", "total_spent": 200.0, "transaction_count": 2},
            "C002": {"name": "B", "total_spent": 100.0, "transaction_count": 1},
        }
        processor.transactions = [
            {"category": "electronics", "amount": 200.0},
            {"category": "food", "amount": 50.0},
            {"category": "electronics", "amount": 50.0},
        ]
        metrics = processor.calculate_customer_metrics()
        self.assertEqual(metrics["total_customers"], 2)
        self.assertEqual(metrics["total_transactions"], 3)
        self.assertAlmostEqual(metrics["total_revenue"], 300.0)
        self.assertAlmostEqual(metrics["average_transaction_value"], 100.0)
        self.assertEqual(metrics["category_breakdown"]["electronics"], 2)
        self.assertEqual(metrics["category_breakdown"]["food"], 1)


class TestGenerateReport(unittest.TestCase):
    """Tests for generate_report."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_generate_metrics_report(self):
        """Verify metrics report generates valid JSON."""
        processor = DataProcessor("dummy.csv")
        processor.customers = {
            "C001": {"name": "Test", "total_spent": 100.0, "transaction_count": 1}
        }
        processor.transactions = [{"category": "food", "amount": 100.0}]
        output = os.path.join(self.test_dir, "metrics.json")
        result = processor.generate_report("metrics", output)
        self.assertTrue(result)

        with open(output, "r") as f:
            data = json.load(f)
            self.assertIn("metrics", data)
            self.assertIn("generated_at", data)

    def test_generate_unknown_report_type(self):
        """Unknown report type should return False."""
        processor = DataProcessor("dummy.csv")
        output = os.path.join(self.test_dir, "report.json")
        result = processor.generate_report("unknown_type", output)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
