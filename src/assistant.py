import os
import pandas as pd

def build_context(df: pd.DataFrame, duplicates: pd.DataFrame) -> str:
    findings = df[df["review_flag"]].copy()

    lines = [
        f"Total vendors: {len(df)}",
        f"Vendors requiring review: {len(findings)}",
        f"Possible duplicate pairs: {len(duplicates)}",
        "",
        "Review records:",
    ]

    for _, r in findings.iterrows():
        lines.append(
            f"{r['vendor_id']} | {r['vendor_name']} | "
            f"score={r['quality_score']} | missing={r['missing_critical_fields']} | "
            f"status={r['status']}"
        )

    return "\n".join(lines)

def deterministic_answer(question: str, df: pd.DataFrame, duplicates: pd.DataFrame) -> str:
    q = question.lower()

    if "duplicate" in q:
        if duplicates.empty:
            return "No possible duplicate pairs were detected by the configured rules."
        result = duplicates.to_string(index=False)
        return "Possible duplicate pairs detected:\n\n" + result

    if "incomplete" in q or "missing" in q:
        cols = ["vendor_id", "vendor_name", "missing_critical_fields", "quality_score"]
        result = df[df["review_flag"]][cols].sort_values("quality_score")
        return "Vendors with data-quality issues:\n\n" + result.to_string(index=False)

    if "risk" in q or "review" in q:
        result = df[["vendor_id", "vendor_name", "quality_score", "review_flag"]].sort_values("quality_score")
        return "Vendor quality review list:\n\n" + result.to_string(index=False)

    if "summary" in q or "overview" in q:
        avg = df["quality_score"].mean()
        return (
            f"Vendor master contains {len(df)} records. "
            f"{int(df['review_flag'].sum())} records require review. "
            f"Average quality score is {avg:.1f}/100. "
            f"{len(duplicates)} possible duplicate pairs were detected."
        )

    return (
        "I can answer questions about vendor completeness, possible duplicates, "
        "quality scores, review flags and overall vendor-master quality. "
        "Try: 'Which vendors have missing fields?'"
    )

def llm_answer(question: str, context: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key or not model:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model,
            instructions=(
                "You are a vendor master data assistant. "
                "Use only the supplied data context. "
                "Do not invent vendor facts. "
                "Explain findings clearly and say when human review is required."
            ),
            input=f"DATA CONTEXT:\n{context}\n\nQUESTION:\n{question}",
        )
        return response.output_text
    except Exception:
        return None
