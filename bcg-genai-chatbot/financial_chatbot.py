#!/usr/bin/env python3
"""
BCG GenAI — AI-Powered Financial Chatbot
A rule-based chatbot for analysing 10-K financial data.

Developer: Mike (Junior Data Scientist, GenAI Consulting Team)
Client: Global Finance Corp. (GFC)
"""

import pandas as pd


class FinancialChatbot:
    """Rule-based financial chatbot with state management and error handling."""

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.companies = [c.lower() for c in data['Company'].unique()]
        self.company_names = {c.lower(): c for c in data['Company'].unique()}
        self.years = sorted(data['Fiscal Year'].unique())

        # State management — remembers conversation context
        self.context = {
            'last_company': None,
            'last_metric': None,
            'last_year': None,
            'query_count': 0,
            'history': [],
        }

        # Map keywords to data columns
        self.metric_map = {
            'revenue': 'Total Revenue',
            'sales': 'Total Revenue',
            'income': 'Net Income',
            'profit': 'Net Income',
            'earnings': 'Net Income',
            'net income': 'Net Income',
            'assets': 'Total Assets',
            'liabilities': 'Total Liabilities',
            'debt': 'Total Liabilities',
            'cash flow': 'Cash Flow from Operations',
            'cash': 'Cash Flow from Operations',
            'operating cash': 'Cash Flow from Operations',
            'margin': 'Profit Margin (%)',
            'profit margin': 'Profit Margin (%)',
            'equity': 'Shareholders Equity',
            'growth': 'Total Revenue Growth (%)',
            'revenue growth': 'Total Revenue Growth (%)',
            'income growth': 'Net Income Growth (%)',
        }

    def _format_currency(self, value):
        if abs(value) >= 1e12:
            return f'${value/1e12:.2f} trillion'
        elif abs(value) >= 1e9:
            return f'${value/1e9:.1f} billion'
        elif abs(value) >= 1e6:
            return f'${value/1e6:.1f} million'
        return f'${value:,.0f}'

    def _detect_company(self, query):
        query_lower = query.lower()
        for key, name in self.company_names.items():
            if key in query_lower:
                return name
        abbrevs = {'msft': 'Microsoft', 'aapl': 'Apple', 'tsla': 'Tesla'}
        for abbrev, name in abbrevs.items():
            if abbrev in query_lower:
                return name
        return self.context['last_company']

    def _detect_metric(self, query):
        query_lower = query.lower()
        for keyword in sorted(self.metric_map.keys(), key=len, reverse=True):
            if keyword in query_lower:
                return self.metric_map[keyword]
        return self.context['last_metric']

    def _detect_year(self, query):
        for year in self.years:
            if str(year) in query:
                return year
        return None

    def _get_metric_data(self, company, metric, year=None):
        company_data = self.data[self.data['Company'] == company]
        if year:
            row = company_data[company_data['Fiscal Year'] == year]
            if row.empty:
                return None
            return row[metric].values[0]
        return company_data[['Fiscal Year', metric]]

    def _generate_trend_insight(self, company, metric):
        company_data = self.data[self.data['Company'] == company].sort_values('Fiscal Year')
        values = company_data[metric].values
        years = company_data['Fiscal Year'].values

        if len(values) < 2:
            return 'Insufficient data for trend analysis.'

        overall_change = ((values[-1] - values[0]) / abs(values[0])) * 100
        latest_change = ((values[-1] - values[-2]) / abs(values[-2])) * 100

        if all(values[i] <= values[i+1] for i in range(len(values)-1)):
            trend = 'consistently increasing'
        elif all(values[i] >= values[i+1] for i in range(len(values)-1)):
            trend = 'consistently declining'
        else:
            trend = 'mixed (fluctuating)'

        is_pct = '%' in metric
        if is_pct:
            values_str = ', '.join([f'FY{y}: {v:.1f}%' for y, v in zip(years, values)])
        else:
            values_str = ', '.join([f'FY{y}: {self._format_currency(v)}' for y, v in zip(years, values)])

        return f"""\n{metric} for {company} (FY{years[0]}-{years[-1]}):
  {values_str}
  Trend: {trend}
  Overall change: {overall_change:+.1f}%
  Latest YoY change: {latest_change:+.1f}%"""

    def _handle_comparison(self, metric, year=None):
        if not year:
            year = max(self.years)

        is_pct = '%' in metric
        results = []
        for company in self.data['Company'].unique():
            value = self._get_metric_data(company, metric, year)
            if value is not None:
                formatted = f'{value:.1f}%' if is_pct else self._format_currency(value)
                results.append((company, value, formatted))

        results.sort(key=lambda x: x[1], reverse=True)

        response = f'\n{metric} comparison for FY{year}:\n'
        for i, (company, value, formatted) in enumerate(results, 1):
            response += f'  {i}. {company}: {formatted}\n'
        response += f'\n  Leader: {results[0][0]}'
        return response

    def _handle_summary(self, company):
        latest_year = max(self.years)
        row = self.data[(self.data['Company'] == company) & (self.data['Fiscal Year'] == latest_year)].iloc[0]

        margin = row['Profit Margin (%)']
        dar = row['Debt to Asset Ratio']

        if margin > 20 and dar < 0.6:
            assessment = 'Strong — high profitability with manageable leverage.'
        elif margin > 10 and dar < 0.7:
            assessment = 'Healthy — solid profitability, leverage within acceptable range.'
        elif margin > 5:
            assessment = 'Moderate — profitable but may face margin or leverage pressure.'
        else:
            assessment = 'Concerning — low margins may indicate operational challenges.'

        response = f"""\nFinancial Summary for {company} (FY{latest_year}):
  Revenue:             {self._format_currency(row['Total Revenue'])}
  Net Income:          {self._format_currency(row['Net Income'])}
  Profit Margin:       {margin:.1f}%
  Total Assets:        {self._format_currency(row['Total Assets'])}
  Total Liabilities:   {self._format_currency(row['Total Liabilities'])}
  Equity:              {self._format_currency(row['Shareholders Equity'])}
  Operating Cash Flow: {self._format_currency(row['Cash Flow from Operations'])}
  Debt-to-Asset Ratio: {dar:.3f}

  Overall Assessment: {assessment}"""
        return response

    def respond(self, user_input: str) -> str:
        self.context['query_count'] += 1
        self.context['history'].append(user_input)
        query = user_input.lower().strip()

        # Greetings
        if query in ['hi', 'hello', 'hey', 'help', 'start']:
            return """Hello! I'm your Financial Analysis Assistant.
I can help you explore financial data for Microsoft, Tesla, and Apple (FY2022-2024).

Here's what I can do:
  - Look up specific metrics (revenue, income, assets, liabilities, cash flow)
  - Show trends over time for any company
  - Compare metrics across companies
  - Provide full financial summaries

What would you like to know?"""

        # Exit
        if query in ['quit', 'exit', 'bye', 'goodbye']:
            return f'Thanks for using the Financial Assistant! You asked {self.context["query_count"]} questions. Goodbye!'

        # Detect intent
        company = self._detect_company(query)
        metric = self._detect_metric(query)
        year = self._detect_year(query)
        is_comparison = any(w in query for w in ['compare', 'comparison', 'vs', 'versus', 'highest', 'lowest', 'best', 'worst', 'rank'])
        is_summary = any(w in query for w in ['summary', 'overview', 'overall', 'health', 'snapshot'])
        is_trend = any(w in query for w in ['trend', 'over time', 'history', 'change', 'grew', 'declined'])

        if company:
            self.context['last_company'] = company
        if metric:
            self.context['last_metric'] = metric

        try:
            if is_summary and company:
                return self._handle_summary(company)
            if is_comparison and metric:
                return self._handle_comparison(metric, year)
            if is_trend and company and metric:
                return self._generate_trend_insight(company, metric)
            if company and metric and year:
                value = self._get_metric_data(company, metric, year)
                if value is not None:
                    is_pct = '%' in metric
                    formatted = f'{value:.1f}%' if is_pct else self._format_currency(value)
                    return f"{company}'s {metric} in FY{year}: {formatted}"
            if company and metric:
                return self._generate_trend_insight(company, metric)
            if company and not metric:
                return f"I can look up data for {company}. What metric are you interested in?\n  Available: revenue, net income, profit margin, assets, liabilities, cash flow"
            if metric and not company:
                return f"Which company would you like to see {metric} for?\n  Available: Microsoft, Tesla, Apple\n  Or say \"compare\" to see all three."

            return """I'm not sure I understood that. I can help with financial data for Microsoft, Tesla, and Apple.
  Try: "Show me Apple's revenue"
  Try: "Compare profit margins"
  Try: "Give me a summary of Tesla"
  Type "help" for more options."""

        except Exception as e:
            return f'Sorry, I encountered an error: {str(e)}\nPlease try rephrasing your question.'


def main():
    """Run the chatbot in interactive mode."""
    df = pd.read_csv('ai_chatbot_data.csv')
    bot = FinancialChatbot(df)

    print(bot.respond('hello'))
    print()

    while True:
        user_input = input('You: ').strip()
        if not user_input:
            continue
        response = bot.respond(user_input)
        print(f'\nBot: {response}\n')
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            break


if __name__ == '__main__':
    main()
