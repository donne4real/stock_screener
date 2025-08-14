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

## Project Structure

```
.
├── app.py              # The Flask backend application
├── screener.py         # Core stock screening logic
├── requirements.txt    # Project dependencies
├── templates
│   └── index.html      # The HTML frontend
└── static
    └── style.css       # CSS for styling the frontend
```
