import json
import os

LEDGER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")

def _load_ledger():
    if not os.path.exists(LEDGER_FILE):
        return []
    with open(LEDGER_FILE, 'r') as f:
        return json.load(f)

def _save_ledger(data):
    with open(LEDGER_FILE, 'w') as f:
        json.dump(data, f)

def add_expense(category, amount):
    ledger = _load_ledger()
    ledger.append({"category": category, "amount": amount})
    _save_ledger(ledger)

def get_spending_by_category():
    ledger = _load_ledger()
    spending = {}
    for entry in ledger:
        cat = entry["category"]
        amount = entry["amount"]
        spending[cat] = spending.get(cat, 0) + amount
    return spending

def check_budget_alert(category, threshold):
    spending = get_spending_by_category()
    return spending.get(category, 0) > threshold
