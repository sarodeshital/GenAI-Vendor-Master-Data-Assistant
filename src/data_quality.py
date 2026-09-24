import pandas as pd

CRITICAL_FIELDS = [
    "tax_id",
    "bank_account",
    "email",
    "phone",
    "address",
    "payment_terms",
]

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    return df

def add_quality_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    missing_count = out[CRITICAL_FIELDS].isna().sum(axis=1)
    out["missing_critical_fields"] = missing_count

    invalid_email = ~out["email"].fillna("").str.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$", na=False
    )
    out["invalid_email"] = invalid_email

    out["quality_score"] = 100 - (missing_count * 12) - (invalid_email.astype(int) * 8)
    out["quality_score"] = out["quality_score"].clip(lower=0)

    out["review_flag"] = out["quality_score"] < 80
    return out

def summary(df: pd.DataFrame) -> dict:
    scored = add_quality_metrics(df)
    return {
        "vendors": int(len(scored)),
        "active": int((scored["status"].str.lower() == "active").sum()),
        "review_required": int(scored["review_flag"].sum()),
        "average_quality_score": round(float(scored["quality_score"].mean()), 1),
        "missing_tax_id": int(scored["tax_id"].isna().sum()),
        "missing_bank_account": int(scored["bank_account"].isna().sum()),
    }
