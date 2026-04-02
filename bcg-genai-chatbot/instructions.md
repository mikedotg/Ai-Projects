# BCG GenAI Job Simulation — Instructions

## Overview

**Platform:** The Forage
**Company:** Boston Consulting Group (BCG)
**Team:** GenAI Consulting Team
**Duration:** 3-4 hours, self-paced
**Skills:** Python, pandas, data analysis, NLP, AI development, financial analysis

---

## Your Role

You are a **junior data scientist** at BCG, part of the GenAI consulting team. You are the newest addition to the team.

**Your Manager:** Aisha — Senior Data Scientist, GenAI Consulting Team

You have been given the responsibility of developing an AI-powered chatbot that analyzes financial documents. This is a cutting-edge project at the intersection of finance and generative AI (GenAI).

---

## The Client

**Global Finance Corp. (GFC)** — a leading global financial institution seeking to enhance its capabilities in analyzing corporate financial performance. Their traditional methods have become time-consuming and less efficient.

GFC wants BCG to develop a tool that can quickly analyze and interpret large sets of financial data, specifically from **10-K and 10-Q reports**.

---

## Project Requirements

- **Efficiency:** Must significantly reduce time to analyze financial documents vs. traditional methods
- **Accuracy:** Chatbot should provide precise and reliable financial insights
- **User-friendly interface:** Intuitive and easy to use regardless of financial expertise
- **Scalability:** Handle increasing number of documents and user queries

**Timeline:** GFC wants implementation in the upcoming financial quarter.

---

## Key Terms

- **10-K reports:** Annual financial reports filed with the SEC by publicly traded companies. Contains audited financial statements, MD&A, and disclosures.
- **10-Q reports:** Quarterly financial reports.
- **GenAI:** A branch of AI focusing on generating new content, including text and data analysis.
- **NLP (Natural Language Processing):** AI technology for understanding and responding to user queries in natural language.

---

## Task 1: Data Extraction and Initial Analysis

### What You'll Learn
- Techniques for extracting key financial data from 10-K documents
- Understanding financial statement components and performance metrics
- Preparing and processing data for AI-driven applications

### What You'll Do
- Extract financial data from provided 10-K documents
- Conduct basic analysis to identify significant financial trends and indicators
- Format and clean the data for further processing in an AI model

### Email Brief from Aisha

> **Subject:** Initiation: Financial Data Analysis for GFC AI Chatbot Project
>
> Your role:
> - **Data extraction:** Research and review 10-K documents. Focus on key financial figures and ratios.
> - **Basic analysis:** Identify significant financial trends and indicators. Assess financial health and performance.
> - **Data preparation:** Format and clean the data for AI model integration.
>
> **Deliverable:** A comprehensive data analysis report including findings and a summary providing insights into the financial health of the analyzed companies.

### Key Sections of 10-K Reports

#### Income Statement
- **Key data points:** Total Revenue, Cost of Goods Sold (COGS), Operating Expenses, Net Income
- **Technique:** Look for income statement summary in early pages. Pay attention to year-over-year changes.

#### Balance Sheet
- **Key data points:** Current Assets, Long-term Assets, Current Liabilities, Long-term Liabilities, Total Shareholders' Equity
- **Technique:** Compare assets against liabilities for financial health. Note large changes.

#### Cash Flow Statement
- **Key data points:** Cash from Operating Activities, Investing Activities, Financing Activities
- **Technique:** Analyze how the company generates and spends cash for liquidity insights.

### Extraction Techniques
1. **Manual extraction:** Review documents to understand layout and key information locations
2. **Highlight and annotate:** Use digital tools to highlight and annotate key figures
3. **Excel/spreadsheet tools:** Input key figures for analysis and comparison
4. **Automated extraction:** Python libraries (Beautiful Soup, Pandas) for digital documents

### Data Preparation Steps

#### Data Cleaning
- Correct or remove incorrect, corrupted, or duplicate data
- Fill missing values, smooth noisy data, resolve inconsistencies

#### Data Transformation
- Normalize and standardize data for AI models
- Convert all figures to consistent format (e.g., all in thousands or millions)
- Adjust for inflation or currency changes where necessary

#### Preprocessing for AI Models
- **Feature engineering:** Create ratios or derive financial health indicators from raw data
- **Data encoding:** Encode categorical data (like fiscal quarters) into numerical values
- **Time-series handling:** Handle trends, seasonality, and lag features

### Step-by-Step Instructions

#### Step 1: Data Extraction
1. Navigate to SEC's EDGAR database:
   - [Microsoft](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K&dateb=&owner=include&count=40)
   - [Tesla](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-K&dateb=&owner=include&count=40)
   - [Apple](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-K&dateb=&owner=include&count=40)
2. For each company, find 10-K filings for the **last three fiscal years**
3. Extract: **Total Revenue, Net Income, Total Assets, Total Liabilities, Cash Flow from Operating Activities**
4. Compile into an Excel spreadsheet

#### Step 2: Preparing Jupyter Notebook Environment
```bash
pip install notebook
jupyter notebook
```
Create a new notebook for analysis.

#### Step 3: Python Analysis in Jupyter
```python
import pandas as pd

# Load data
df = pd.read_csv('path_to_your_csv_file.csv')

# Year-over-year changes
df['Revenue Growth (%)'] = df.groupby(['Company'])['Total Revenue'].pct_change() * 100
df['Net Income Growth (%)'] = df.groupby(['Company'])['Net Income'].pct_change() * 100
```
- Explore aggregate functions and groupings (by company, over years, etc.)
- Use markdown cells for narrative explanations

#### Step 4: Documentation and Submission
- Document methodology, observations, and conclusions using markdown in Jupyter
- Export notebook as PDF or HTML
- **Upload your Jupyter Notebook**

### Resource
- [How to Read a 10-K](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read)

---

## Task 2: AI-Powered Financial Chatbot Development

*(Instructions to be added when available)*

---

## Future Idea

Create our own AI tests and quizzes from what we learn in these simulations to teach others.
