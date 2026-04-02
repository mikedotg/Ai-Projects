# BCG GenAI — AI-Powered Financial Chatbot

## How It Works

This chatbot analyses 10-K financial data for Microsoft, Tesla, and Apple (FY2022-2024) and responds to user queries using rule-based logic.

### Architecture

1. **Intent Detection** — Keywords identify what the user wants (data point, trend, comparison, summary)
2. **Entity Extraction** — Detects company names, metrics, and fiscal years from natural language
3. **Data Retrieval** — Fetches the right data from the structured CSV
4. **Response Generation** — Formats raw numbers into readable insights with context

### Predefined Query Types

| Query Type | Example | What It Returns |
|---|---|---|
| Specific lookup | "Apple's revenue in 2024" | Single formatted value |
| Trend analysis | "Tesla's revenue trend" | Multi-year values, direction, % change |
| Comparison | "Compare profit margins" | Ranked list across all companies |
| Summary | "Summary of Microsoft" | Full financial snapshot with health assessment |
| Follow-up | "What about cash flow?" | Uses last-mentioned company from context |

### Supported Metrics

revenue, net income, profit, earnings, assets, liabilities, debt, cash flow, profit margin, equity, growth

### State Management

The chatbot remembers the last company and metric discussed, enabling natural follow-up questions without repeating context.

### Error Handling

Unrecognised queries return helpful suggestions rather than error messages, guiding users toward valid queries.

## How to Run

```bash
pip install pandas
python financial_chatbot.py
```

## Limitations

- Rule-based only — cannot handle truly open-ended questions
- Limited to 3 companies and 3 fiscal years
- No NLP — relies on keyword matching (e.g., "profit" works but "how much money did they make" does not)
- Text-only — no chart generation in the CLI version
- No real-time data — uses static CSV extracted from SEC EDGAR

## Files

- `financial_chatbot.py` — Standalone chatbot script
- `bcg_financial_chatbot.ipynb` — Jupyter notebook with full development and testing
- `ai_chatbot_data.csv` — Cleaned financial data used by the chatbot
- `financial_data.csv` — Raw extracted data from 10-K filings
