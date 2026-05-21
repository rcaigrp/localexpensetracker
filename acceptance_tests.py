import json
import os
import pytest
import expense_tracker

@pytest.fixture
def clean_ledger():
    ledger_path = os.path.join(os.path.dirname(os.path.abspath(expense_tracker.__file__)), "ledger.json")
    if os.path.exists(ledger_path):
        os.remove(ledger_path)
    yield
    if os.path.exists(ledger_path):
        os.remove(ledger_path)

def test_criterion_1_module_exists():
    import expense_tracker
    assert True

def test_criterion_2_add_expense(clean_ledger):
    expense_tracker.add_expense("food", 10.0)
    expense_tracker.add_expense("food", 20.0)
    expense_tracker.add_expense("transport", 15.0)
    assert os.path.exists(os.path.join(os.path.dirname(os.path.abspath(expense_tracker.__file__)), "ledger.json"))
    with open(os.path.join(os.path.dirname(os.path.abspath(expense_tracker.__file__)), "ledger.json"), "r") as f:
        ledger = json.load(f)
    assert len(ledger) == 3
    assert ledger[0]["category"] == "food"
    assert ledger[0]["amount"] == 10.0

def test_criterion_3_get_spending_by_category(clean_ledger):
    expense_tracker.add_expense("food", 10.0)
    expense_tracker.add_expense("food", 20.0)
    expense_tracker.add_expense("transport", 15.0)
    result = expense_tracker.get_spending_by_category()
    assert result == {"food": 30.0, "transport": 15.0}

def test_criterion_4_check_budget_alert(clean_ledger):
    expense_tracker.add_expense("food", 50.0)
    expense_tracker.add_expense("transport", 30.0)
    assert expense_tracker.check_budget_alert(100.0) == False
    assert expense_tracker.check_budget_alert(50.0) == True
