import pandas as pd
from src.data_quality import add_quality_metrics
from src.duplicate_detection import find_possible_duplicates

def test_quality_score_detects_missing_fields():
    df = pd.DataFrame([{
        "vendor_id": "V1",
        "vendor_name": "Test Vendor",
        "country": "India",
        "city": "Pune",
        "tax_id": None,
        "bank_account": None,
        "email": "test@example.com",
        "phone": "123",
        "address": "Pune",
        "status": "Active",
        "payment_terms": 30,
        "last_updated": "2026-01-01",
    }])
    result = add_quality_metrics(df)
    assert result.loc[0, "missing_critical_fields"] == 2
    assert result.loc[0, "review_flag"] is True

def test_duplicate_detection():
    df = pd.DataFrame([
        {"vendor_id": "V1", "vendor_name": "Northstar Logistics", "tax_id": "T1", "bank_account": "B1"},
        {"vendor_id": "V2", "vendor_name": "North Star Logistics Ltd", "tax_id": "T1", "bank_account": "B1"},
    ])
    result = find_possible_duplicates(df)
    assert len(result) == 1
