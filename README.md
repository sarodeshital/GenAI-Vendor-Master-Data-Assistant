# GenAI Vendor Master Data Assistant

An end-to-end GenAI + data-quality project for analyzing vendor master data, identifying potential data-quality issues, explaining duplicate/similar vendors, and answering vendor-related questions using a natural-language assistant.

## Business Problem

Vendor master data often contains duplicate vendors, incomplete tax/bank/contact information, inconsistent naming, inactive vendors, and conflicting records. These issues can create payment delays, reporting problems, and control/audit risks.

This project demonstrates a practical assistant that:

1. Loads vendor master data.
2. Runs deterministic data-quality checks.
3. Creates a vendor risk/quality score.
4. Uses fuzzy matching to find possible duplicate vendors.
5. Generates human-readable explanations.
6. Provides a Streamlit GenAI-style chat interface.
7. Optionally connects to an LLM through an API.
8. Works in demo mode without an API key.

> Important: The project flags records for review. It does not declare fraud or wrongdoing.

## Architecture

CSV / SQL data
      |
      v
Data validation + cleaning
      |
      +----> Duplicate detection
      |
      +----> Completeness checks
      |
      +----> Status / control checks
      |
      v
Vendor Quality Engine
      |
      +----> Dashboard metrics
      |
      +----> Findings / explanations
      |
      v
GenAI Vendor Master Data Assistant
      |
      +----> Natural-language Q&A
      +----> Suggested investigation actions

## Tech Stack

- Python
- Pandas
- Streamlit
- RapidFuzz
- SQLite
- SQL
- Optional OpenAI-compatible LLM API
- Git/GitHub

## Project Structure

```text
genai-vendor-master-data-assistant/
├── data/
│   └── vendor_master.csv
├── docs/
│   └── sample_questions.md
├── sql/
│   └── vendor_quality.sql
├── src/
│   ├── assistant.py
│   ├── data_quality.py
│   ├── duplicate_detection.py
│   └── database.py
├── tests/
│   └── test_quality.py
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run Locally

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/genai-vendor-master-data-assistant.git
cd genai-vendor-master-data-assistant
```

### 2. Create environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### 3. Install

```bash
pip install -r requirements.txt
```

### 4. Start application

```bash
streamlit run app.py
```

The app runs in demo mode without an API key.

## Optional LLM Configuration

Copy `.env.example` to `.env` and add your API configuration.

The application is designed so the deterministic data-quality engine remains the source of truth. The LLM is used to turn findings into natural-language explanations rather than inventing vendor facts.

## Example Questions

- Which vendors have incomplete master data?
- Show vendors with high data-quality risk.
- Are there possible duplicate vendors?
- Why was vendor V1008 flagged?
- Summarize the main vendor master issues.
- What fields should be reviewed before vendor activation?

## Interview Explanation

### 30-second version

"I built a GenAI Vendor Master Data Assistant that combines Python data-quality rules, fuzzy duplicate detection, SQL analysis and a natural-language assistant. It checks vendor master records for missing critical fields, invalid values, inactive records and possible duplicates. The GenAI layer converts those findings into explanations and recommended investigation steps. I deliberately kept the quality engine deterministic so the LLM doesn't invent business facts."

### Key technical points

- Pandas for validation and profiling
- RapidFuzz for approximate vendor-name matching
- SQLite/SQL for analytical queries
- Streamlit for the application
- LLM-ready assistant architecture
- Explainable quality scoring
- Synthetic data to avoid exposing confidential vendor information

## Resume Bullet

**GenAI Vendor Master Data Assistant | Python, SQL, Streamlit, GenAI, RapidFuzz**
- Built an end-to-end GenAI assistant for vendor master-data quality analysis, combining Python validation, SQL analytics and fuzzy duplicate detection to identify incomplete and potentially duplicate vendor records.
- Developed an explainable vendor quality scoring framework and natural-language interface that summarizes findings and suggests investigation actions while keeping deterministic data-quality checks as the source of truth.
