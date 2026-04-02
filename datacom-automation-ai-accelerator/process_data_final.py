#!/usr/bin/env python3
"""
Data Processing Script for Customer Analytics (Refactored)

Original: process_data.py — contained bugs and performance issues.
This version fixes the export bug, improves performance, and adds
proper input validation throughout.

Changes made:
- Fixed export_customer_data: empty customers no longer silently writes
  an empty file; corrupted records are validated before export.
- Renamed 'format' parameter to 'output_format' to avoid shadowing
  Python's built-in format() function.
- Replaced manual category counting with collections.Counter for
  better performance.
- Added explicit fieldnames list instead of fragile dynamic extraction.
- Added data validation in load_data and process_transactions.
"""

import csv
import json
import logging
from collections import Counter
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define expected customer fields in one place for consistency
CUSTOMER_FIELDS = ["customer_id", "name", "email", "join_date", "total_spent", "transaction_count"]


class DataProcessor:
    """Processes customer transaction data and generates analytics reports."""

    def __init__(self, input_file: str):
        """Initialize the data processor with input file path."""
        self.input_file = input_file
        self.customers: Dict[str, Dict[str, Any]] = {}
        self.transactions: List[Dict[str, Any]] = []
        self.reports: Dict[str, Any] = {}

    def load_data(self) -> bool:
        """Load customer data from CSV file.

        Validates that required fields (customer_id, name, email, join_date)
        are present in each row before adding to the customers dict.
        """
        try:
            with open(self.input_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Validate required fields exist
                    if not all(
                        key in row for key in ["customer_id", "name", "email", "join_date"]
                    ):
                        logger.warning(f"Skipping malformed customer row: {row}")
                        continue

                    customer_id = row["customer_id"]
                    self.customers[customer_id] = {
                        "name": row["name"],
                        "email": row["email"],
                        "join_date": row["join_date"],
                        "total_spent": 0.0,
                        "transaction_count": 0,
                    }
            logger.info(f"Loaded {len(self.customers)} customers")
            return True
        except FileNotFoundError:
            logger.error(f"Input file {self.input_file} not found")
            return False
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False

    def process_transactions(self, transaction_file: str) -> bool:
        """Process transaction data and update customer records.

        Validates each transaction row has required fields and a valid
        numeric amount before processing.
        """
        try:
            with open(transaction_file, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Validate required fields
                    required = ["transaction_id", "customer_id", "amount", "date", "category"]
                    if not all(key in row for key in required):
                        logger.warning(f"Skipping malformed transaction row: {row}")
                        continue

                    try:
                        amount = float(row["amount"])
                    except (ValueError, TypeError):
                        logger.warning(
                            f"Invalid amount in transaction {row.get('transaction_id', '?')}: {row.get('amount')}"
                        )
                        continue

                    transaction = {
                        "transaction_id": row["transaction_id"],
                        "customer_id": row["customer_id"],
                        "amount": amount,
                        "date": row["date"],
                        "category": row["category"],
                    }
                    self.transactions.append(transaction)

                    # Update customer totals
                    customer_id = row["customer_id"]
                    if customer_id in self.customers:
                        self.customers[customer_id]["total_spent"] += amount
                        self.customers[customer_id]["transaction_count"] += 1
                    else:
                        logger.warning(
                            f"Transaction for unknown customer: {customer_id}"
                        )

            logger.info(f"Processed {len(self.transactions)} transactions")
            return True
        except FileNotFoundError:
            logger.error(f"Transaction file {transaction_file} not found")
            return False
        except Exception as e:
            logger.error(f"Error processing transactions: {e}")
            return False

    def calculate_customer_metrics(self) -> Dict[str, Any]:
        """Calculate customer metrics and statistics.

        Performance improvement: uses collections.Counter for category
        breakdown instead of manual dict building.
        """
        if not self.customers:
            logger.error("No customer data available")
            return {}

        total_revenue = sum(
            cust["total_spent"] for cust in self.customers.values()
        )
        total_transactions = len(self.transactions)

        metrics = {
            "total_customers": len(self.customers),
            "total_transactions": total_transactions,
            "total_revenue": total_revenue,
            "average_transaction_value": (
                total_revenue / total_transactions if total_transactions > 0 else 0.0
            ),
            "top_customers": sorted(
                self.customers.items(),
                key=lambda x: x[1]["total_spent"],
                reverse=True,
            )[:10],
            "category_breakdown": dict(
                Counter(t["category"] for t in self.transactions)
            ),
        }

        return metrics

    def find_matches(
        self, search_term: str, field: str = "name"
    ) -> List[Dict[str, Any]]:
        """Find customers matching the search term in the specified field."""
        matches = []
        search_term_lower = search_term.lower()

        for customer_id, customer_data in self.customers.items():
            if field in customer_data:
                field_value = str(customer_data[field]).lower()
                if search_term_lower in field_value:
                    matches.append({"customer_id": customer_id, **customer_data})

        return matches

    def generate_report(self, report_type: str, output_file: str) -> bool:
        """Generate various types of reports and save to file."""
        try:
            if report_type == "customer_summary":
                report_data = {
                    "generated_at": datetime.now().isoformat(),
                    "customers": list(self.customers.values()),
                }
            elif report_type == "metrics":
                report_data = {
                    "generated_at": datetime.now().isoformat(),
                    "metrics": self.calculate_customer_metrics(),
                }
            elif report_type == "transactions":
                report_data = {
                    "generated_at": datetime.now().isoformat(),
                    "transactions": self.transactions,
                }
            else:
                logger.error(f"Unknown report type: {report_type}")
                return False

            with open(output_file, "w") as file:
                json.dump(report_data, file, indent=2)

            logger.info(f"Generated {report_type} report: {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return False

    def export_customer_data(self, output_file: str, output_format: str = "csv") -> bool:
        """Export customer data in specified format.

        Fixes from original:
        - Renamed 'format' parameter to 'output_format' (avoids shadowing built-in).
        - Uses explicit CUSTOMER_FIELDS list instead of fragile
          next(iter(self.customers.values())).keys() extraction.
        - Validates that customers dict is not empty before CSV export.
        - Validates each customer record is a dict before writing.
        """
        try:
            if not self.customers:
                logger.warning("No customer data to export")
                return False

            if output_format == "csv":
                with open(output_file, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=CUSTOMER_FIELDS)
                    writer.writeheader()

                    for customer_id, data in self.customers.items():
                        if not isinstance(data, dict):
                            logger.warning(
                                f"Skipping corrupted record for customer {customer_id}"
                            )
                            continue
                        row = {"customer_id": customer_id, **data}
                        writer.writerow(row)

            elif output_format == "json":
                with open(output_file, "w") as file:
                    json.dump(self.customers, file, indent=2)
            else:
                logger.error(f"Unsupported format: {output_format}")
                return False

            logger.info(f"Exported customer data to {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return False


def main():
    """Main function to run the data processing pipeline."""
    processor = DataProcessor("customers.csv")

    if not processor.load_data():
        logger.error("Failed to load customer data")
        return

    if not processor.process_transactions("transactions.csv"):
        logger.error("Failed to process transactions")
        return

    # Generate reports
    processor.generate_report("customer_summary", "customer_summary.json")
    processor.generate_report("metrics", "metrics.json")
    processor.generate_report("transactions", "transactions.json")

    # Export data
    processor.export_customer_data("customers_export.csv", "csv")
    processor.export_customer_data("customers_export.json", "json")

    logger.info("Data processing completed successfully")


if __name__ == "__main__":
    main()
