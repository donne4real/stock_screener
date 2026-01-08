# Benjamin Graham Stock Screener

This project is a web-based stock screening tool that analyzes S&P 500 companies based on a simplified set of investment criteria inspired by Benjamin Graham's value investing philosophy. The application provides an easy-to-use interface to run the screener and view the results.

## Features

-   Fetches the current list of S&P 500 tickers from Wikipedia.
-   Applies a series of simplified Graham-inspired filters to each stock.
-   Displays the results in a clear, user-friendly web interface.
-   Shows which stocks passed all the screening criteria.
-   Provides detailed reasons for why a stock passed or failed each filter.

## Graham-Inspired Filters

The screener uses the following simplified filters based on Benjamin Graham's principles for identifying undervalued stocks:

1.  **Earnings Stability**: Positive earnings for the last 5 consecutive years. This filter aims to identify companies with a consistent track record of profitability.
2.  **Current Ratio**: Current Assets / Current Liabilities >= 2.0. A strong current ratio suggests that the company has a healthy buffer of short-term assets to cover its short-term liabilities.
3.  **Debt-to-Equity Ratio**: Total Debt / Shareholder Equity < 1.0. This filter favors companies that are not heavily reliant on debt to finance their operations.
4.  **Valuation (P/E and P/B Ratios)**:
    -   Price-to-Earnings (P/E) Ratio < 15
    -   Price-to-Book (P/B) Ratio < 1.5
    These valuation metrics help identify stocks that may be trading at a discount to their intrinsic value.

**Disclaimer**: This is a simplified educational tool and not financial advice. The filters used are a basic interpretation of Graham's principles and do not cover all aspects of his investment strategy. Always do your own research before making any investment decisions.

## Market Audit Tool

In addition to the web-based screener, this project includes a standalone command-line script `market_audit.py` that performs a comprehensive multi-model audit on a broader set of tickers (NASDAQ and others).

### Audit Metrics

This tool calculates and evaluates stocks based on:

1.  **Net-Net (Graham)**: Checks if the stock price is less than 2/3rds of its Net Current Asset Value (NCAV) per share.
2.  **Acquirer's Multiple**: Looks for an EV/EBIT multiple of less than 10.
3.  **Piotroski F-Score**: Calculates the F-Score (0-9) to assess financial strength. A score of 7 or higher is considered strong.
4.  **Dividend Yield**: Checks for a dividend yield greater than 3%.
5.  **Price-to-Book (P/B)**: Checks for a P/B ratio less than 1.2.

The script generates an Excel file (e.g., `Market_Audit_YYYYMMDD_HHMM.xlsx`) containing the metrics for stocks that pass at least one of the major criteria.

## Getting Started

### Prerequisites

-   Python 3.6 or higher
-   pip (Python package installer)

### Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone https://github.com/your-username/graham-stock-screener.git
    cd graham-stock-screener
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the Flask web server**:
    ```bash
    python app.py
    ```

2.  **Open your web browser** and navigate to:
    ```
    http://127.0.0.1:5000
    ```

3.  **Click the "Run Screener" button** to start the analysis. Please be patient, as it may take a few minutes to screen all S&P 500 stocks. The results will be displayed on the page once the process is complete.

### Running the Market Audit

To run the standalone market audit script:

```bash
python market_audit.py
```

This will output the progress to the console and save the results to an Excel file in the current directory.

## Project Structure

```
.
├── app.py              # The Flask backend application
├── screener.py         # Core stock screening logic
├── market_audit.py     # Standalone multi-model stock audit script
├── requirements.txt    # Project dependencies
├── templates
│   └── index.html      # The HTML frontend
└── static
    └── style.css       # CSS for styling the frontend
```
