from rapidfuzz.fuzz import ratio
import pandas as pd

def find_possible_duplicates(df: pd.DataFrame, threshold: int = 88) -> pd.DataFrame:
    rows = []
    data = df.reset_index(drop=True)

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            a = data.loc[i]
            b = data.loc[j]

            name_score = ratio(str(a["vendor_name"]).lower(), str(b["vendor_name"]).lower())
            tax_match = bool(
                pd.notna(a["tax_id"]) and pd.notna(b["tax_id"]) and a["tax_id"] == b["tax_id"]
            )
            bank_match = bool(
                pd.notna(a["bank_account"])
                and pd.notna(b["bank_account"])
                and a["bank_account"] == b["bank_account"]
            )

            if name_score >= threshold or tax_match or bank_match:
                rows.append({
                    "vendor_1": a["vendor_id"],
                    "vendor_2": b["vendor_id"],
                    "name_similarity": round(name_score, 1),
                    "tax_id_match": tax_match,
                    "bank_account_match": bank_match,
                    "reason": "Name similarity" if name_score >= threshold else
                             ("Same tax ID" if tax_match else "Same bank account")
                })

    return pd.DataFrame(rows)
