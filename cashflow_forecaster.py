"""
MSME UPI Cash-Flow Forecaster
Simple starter script for Indian MSMEs to categorize UPI transactions
and forecast 30-day cash flow.

Usage: python cashflow_forecaster.py
"""

from datetime import datetime, timedelta
from collections import defaultdict
import random

# Sample UPI-style transactions (replace with real CSV export)
SAMPLE_TRANSACTIONS = [
    {"date": "2026-11-01", "description": "UPI/NEFT from Customer ABC Traders", "amount": 45000, "type": "credit"},
    {"date": "2026-11-02", "description": "UPI payment to Supplier XYZ Materials", "amount": -18500, "type": "debit"},
    {"date": "2026-11-03", "description": "GST payment to Government", "amount": -7200, "type": "debit"},
    {"date": "2026-11-05", "description": "UPI from Retail Customer Shop 12", "amount": 12800, "type": "credit"},
    {"date": "2026-11-07", "description": "Salary payment to staff", "amount": -25000, "type": "debit"},
    {"date": "2026-11-10", "description": "UPI/NEFT from Customer ABC Traders", "amount": 32000, "type": "credit"},
    {"date": "2026-11-12", "description": "UPI to logistics partner", "amount": -5600, "type": "debit"},
    {"date": "2026-11-15", "description": "UPI from new customer order", "amount": 27500, "type": "credit"},
    {"date": "2026-11-18", "description": "Electricity bill payment", "amount": -4100, "type": "debit"},
]

# Open invoices (for matching)
OPEN_INVOICES = [
    {"customer": "ABC Traders", "amount": 45000, "invoice_no": "INV-1045", "due_date": "2026-11-05"},
    {"customer": "ABC Traders", "amount": 32000, "invoice_no": "INV-1052", "due_date": "2026-11-12"},
    {"customer": "Retail Customer Shop 12", "amount": 12800, "invoice_no": "INV-1048", "due_date": "2026-11-08"},
]

def categorize_transaction(description: str, amount: float) -> str:
    """
    Simple rule-based categorizer.
    In production, replace with an ML model trained on MSME transaction text.
    """
    desc = description.lower()
    if any(word in desc for word in ["gst", "tax", "government"]):
        return "GST / Tax"
    if any(word in desc for word in ["salary", "staff", "payroll"]):
        return "Salary"
    if any(word in desc for word in ["supplier", "materials", "vendor", "logistics"]):
        return "Vendor / COGS"
    if any(word in desc for word in ["electricity", "bill", "utility"]):
        return "Utilities"
    if amount > 0:
        return "Sales / Inflow"
    return "Other Expense"

def match_invoices(transactions):
    """Match credit transactions to open invoices (simple exact amount match)."""
    matched = []
    for txn in transactions:
        if txn["amount"] <= 0:
            continue
        for inv in OPEN_INVOICES:
            if abs(txn["amount"] - inv["amount"]) < 1:  # exact match
                matched.append({
                    "transaction": txn,
                    "invoice": inv,
                    "status": "Matched"
                })
                break
    return matched

def forecast_cashflow(transactions, days=30, starting_balance=50000):
    """
    Generate a simple 30-day cash flow forecast.
    Assumes historical average daily net + some expected inflows.
    """
    # Calculate historical daily net
    daily_nets = defaultdict(float)
    for txn in transactions:
        daily_nets[txn["date"]] += txn["amount"]
    
    avg_daily_net = sum(daily_nets.values()) / max(len(daily_nets), 1)
    
    forecast = []
    current_balance = starting_balance
    today = datetime(2026, 11, 19)
    
    for i in range(days):
        date = today + timedelta(days=i)
        # Simple projection: average + some randomness for demo
        projected_net = avg_daily_net * 0.8 + random.uniform(-2000, 4000)
        current_balance += projected_net
        forecast.append({
            "date": date.strftime("%Y-%m-%d"),
            "projected_net": round(projected_net, 2),
            "balance": round(current_balance, 2)
        })
    return forecast

def main():
    print("=" * 60)
    print("MSME UPI Cash-Flow Forecaster")
    print("=" * 60)
    
    # Categorize
    print("\n📊 Categorized Transactions:")
    print("-" * 60)
    for txn in SAMPLE_TRANSACTIONS:
        category = categorize_transaction(txn["description"], txn["amount"])
        print(f"{txn['date']} | {category:15} | ₹{txn['amount']:>10,} | {txn['description'][:40]}")
    
    # Match invoices
    print("\n📋 Invoice Matching:")
    print("-" * 60)
    matches = match_invoices(SAMPLE_TRANSACTIONS)
    for m in matches:
        print(f"✓ ₹{m['transaction']['amount']:,} matched to {m['invoice']['invoice_no']} ({m['invoice']['customer']})")
    
    if not matches:
        print("No exact matches found in sample data.")
    
    # Forecast
    print("\n📈 30-Day Cash Flow Forecast (starting balance: ₹50,000):")
    print("-" * 60)
    forecast = forecast_cashflow(SAMPLE_TRANSACTIONS)
    
    shortfall_days = []
    for day in forecast[:7]:  # show first week in detail
        status = "⚠️ SHORTFALL" if day["balance"] < 10000 else "✓ OK"
        print(f"{day['date']} | Balance: ₹{day['balance']:>10,} | {status}")
        if day["balance"] < 10000:
            shortfall_days.append(day["date"])
    
    print("\n... (showing first 7 days)")
    
    if shortfall_days:
        print(f"\n⚠️ Potential shortfall alert on: {', '.join(shortfall_days)}")
        print("Recommendation: Accelerate collections or arrange short-term working capital.")
    else:
        print("\n✓ Cash position looks healthy for the forecast period.")
    
    print("\n" + "=" * 60)
    print("Tip: Replace SAMPLE_TRANSACTIONS with your real UPI CSV export.")
    print("This script is ready to be extended with ML categorization models.")

if __name__ == "__main__":
    main()
