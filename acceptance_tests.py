import pytest
import os
import json

PROJECT_DIR = "/workspace/projects/LocalExpenseTracker"
LEDGER_FILE = os.path.join(PROJECT_DIR, "expenses.json")

@pytest.fixture
def clean_ledger():
    if os.path.exists(LEDGER_FILE):
        os.remove(LEDGER_FILE)
    yield
    if os.path.exists(LEDGER_FILE):
        os.remove(LEDGER_FILE)

def test_criterion_1_import():
    try:
        import expense_tracker
        assert True
    except ImportError:
        assert False

def test_criterion_2_add_expense(clean_ledger):
    import expense_tracker
    expense_tracker.add_expense("food", 10.50)
    assert os.path.exists(LEDGER_FILE)
    with open(LEDGER_FILE, 'r') as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["category"] == "food"
    assert data[0]["amount"] == 10.50

def test_criterion_3_get_spending_by_category(clean_ledger):
    import expense_tracker
    expense_tracker.add_expense("food", 10.0)
    expense_tracker.add_expense("food", 20.0)
    expense_tracker.add_expense("transport", 15.0)
    result = expense_tracker.get_spending_by_category()
    assert result == {"food": 30.0, "transport": 15.0}

def test_criterion_4_check_budget_alert(clean_ledger):
    import expense_tracker
    expense_tracker.add_expense("food", 100.0)
    assert expense_tracker.check_budget_alert("food", 50.0) == True
    assert expense_tracker.check_budget_alert("food", 100.0) == False
    assert expense_tracker.check_budget_alert("food", 101.0) == False
