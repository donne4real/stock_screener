import yfinance as yf
import pandas as pd
import numpy as np
import time
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def get_sp500_tickers():
    """
    Scrapes the list of S&P 500 tickers from Wikipedia.
    Returns a list of ticker symbols.
    """
    print("Fetching S&P 500 tickers from Wikipedia...")
    try:
        table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        df = table[0]
        tickers = df['Symbol'].tolist()
        print(f"Successfully retrieved {len(tickers)} S&P 500 tickers.")
        return tickers
    except Exception as e:
        print(f"Error fetching S&P 500 tickers: {e}")
        return []

def apply_graham_filters(ticker):
    """
    Applies a set of simplified Benjamin Graham-inspired filters to a stock.
    Returns a dictionary of filter results and a boolean indicating if all passed.
    """
    print(f"\n--- Applying Graham Filters for {ticker} ---")

    results = {
        "ticker": ticker,
        "passed_all": False,
        "filters": {}
    }

    try:
        # Get Ticker object and financial data
        stock = yf.Ticker(ticker)
        info = stock.info
        bs_annual = stock.balance_sheet
        is_annual = stock.income_stmt

        # Check if essential data is available
        if bs_annual.empty or is_annual.empty:
            results["error"] = "Essential financial statements are not available."
            return results

        # Transpose so rows are metrics and columns are years
        bs_annual = bs_annual.T
        is_annual = is_annual.T

        # --- Filter 1: Earnings Stability (Positive earnings for the last 5 years) ---
        try:
            last_5_years_earnings = is_annual['Net Income'].head(5)
            if len(last_5_years_earnings) < 5:
                results["filters"]["earnings_stability"] = {"passed": False, "reason": "Less than 5 years of earnings data available."}
            elif (last_5_years_earnings > 0).all():
                results["filters"]["earnings_stability"] = {"passed": True, "reason": f"Positive net income for the last 5 years."}
            else:
                results["filters"]["earnings_stability"] = {"passed": False, "reason": "Net income was not consistently positive."}
        except KeyError:
            results["filters"]["earnings_stability"] = {"passed": False, "reason": "Net Income data not found."}

        # --- Filter 2: Current Ratio (Current Assets / Current Liabilities >= 2.0) ---
        try:
            current_assets = bs_annual.iloc[0].get('Total Current Assets')
            current_liabilities = bs_annual.iloc[0].get('Total Current Liabilities')

            if pd.isna(current_assets) or pd.isna(current_liabilities) or current_liabilities == 0:
                results["filters"]["current_ratio"] = {"passed": False, "reason": "Current assets or liabilities data missing or zero."}
            else:
                current_ratio = current_assets / current_liabilities
                if current_ratio >= 2.0:
                    results["filters"]["current_ratio"] = {"passed": True, "reason": f"Current Ratio: {current_ratio:.2f} >= 2.0."}
                else:
                    results["filters"]["current_ratio"] = {"passed": False, "reason": f"Current Ratio: {current_ratio:.2f} < 2.0."}
        except KeyError:
            results["filters"]["current_ratio"] = {"passed": False, "reason": "Required balance sheet data missing."}

        # --- Filter 3: Debt-to-Equity Ratio (Total Debt / Shareholder Equity < 1.0) ---
        try:
            total_liabilities = bs_annual.iloc[0].get('Total Liabilities Net Minority Interest')
            shareholder_equity = bs_annual.iloc[0].get('Total Equity Gross Minority Interest')

            if pd.isna(total_liabilities) or pd.isna(shareholder_equity) or shareholder_equity <= 0:
                results["filters"]["debt_to_equity"] = {"passed": False, "reason": "Debt or equity data missing or equity is non-positive."}
            else:
                debt_to_equity = total_liabilities / shareholder_equity
                if debt_to_equity < 1.0:
                    results["filters"]["debt_to_equity"] = {"passed": True, "reason": f"Debt-to-Equity: {debt_to_equity:.2f} < 1.0."}
                else:
                    results["filters"]["debt_to_equity"] = {"passed": False, "reason": f"Debt-to-Equity: {debt_to_equity:.2f} >= 1.0."}
        except KeyError:
            results["filters"]["debt_to_equity"] = {"passed": False, "reason": "Required balance sheet data missing."}

        # --- Filter 4: P/E Ratio (< 15) and P/B Ratio (< 1.5) ---
        try:
            pe_ratio = info.get('trailingPE')
            pb_ratio = info.get('priceToBook')

            if pd.isna(pe_ratio) or pd.isna(pb_ratio):
                results["filters"]["pe_pb_ratio"] = {"passed": False, "reason": "P/E or P/B ratio data missing."}
            elif pe_ratio < 15 and pb_ratio < 1.5:
                 results["filters"]["pe_pb_ratio"] = {"passed": True, "reason": f"P/E: {pe_ratio:.2f} < 15 AND P/B: {pb_ratio:.2f} < 1.5."}
            else:
                reasons = []
                if pe_ratio >= 15:
                    reasons.append(f"P/E: {pe_ratio:.2f} >= 15")
                if pb_ratio >= 1.5:
                    reasons.append(f"P/B: {pb_ratio:.2f} >= 1.5")
                results["filters"]["pe_pb_ratio"] = {"passed": False, "reason": " and ".join(reasons)}
        except Exception as e:
             results["filters"]["pe_pb_ratio"] = {"passed": False, "reason": f"Error calculating P/E and P/B: {e}"}

        # Check if all filters passed
        all_passed = all(f["passed"] for f in results["filters"].values())
        results["passed_all"] = all_passed

    except Exception as e:
        results["error"] = f"An unexpected error occurred: {e}"

    return results

def save_results_to_spreadsheet(results, filename='graham_screener_results.xlsx'):
    """
    Saves the screening results to an Excel spreadsheet.
    """
    print(f"\nSaving results to '{filename}'...")

    # Create a list of dictionaries to store flattened results for a DataFrame
    flat_results = []
    for stock in results:
        row = {'Ticker': stock['ticker'], 'Passed All': 'Yes' if stock['passed_all'] else 'No'}
        if 'error' in stock:
            row['Error'] = stock['error']
        else:
            for filter_name, filter_result in stock['filters'].items():
                row[f'{filter_name.title()} Status'] = 'PASS' if filter_result['passed'] else 'FAIL'
                row[f'{filter_name.title()} Reason'] = filter_result['reason']
        flat_results.append(row)

    df = pd.DataFrame(flat_results)

    try:
        # Write the DataFrame to an Excel file
        df.to_excel(filename, index=False)
        print("Results saved successfully! ✅")

    except Exception as e:
        print(f"Error saving to spreadsheet: {e}")

def main():
    # Get the list of S&P 500 tickers
    tickers_to_check = get_sp500_tickers()
    if not tickers_to_check:
        print("Could not retrieve tickers. Exiting.")
        return

    all_results = []
    passing_stocks = []

    for ticker in tickers_to_check:
        # A small delay is crucial to avoid being rate-limited by Yahoo Finance
        time.sleep(1)
        filter_results = apply_graham_filters(ticker)
        all_results.append(filter_results)

        if "error" in filter_results:
            print(f"Skipping {ticker} due to an error: {filter_results['error']}")
            continue

        if filter_results.get("passed_all"):
            passing_stocks.append(filter_results)

    # --- Final Summary ---
    print("\n" + "="*50)
    print("      SUMMARY OF GRAHAM SCREENER RESULTS")
    print("="*50)

    if passing_stocks:
        print(f"\n🏆 Stocks Passing ALL Graham Criteria ({len(passing_stocks)} total):")
        for stock in passing_stocks:
            print(f"  - {stock['ticker']}")
    else:
        print("\n❌ No stocks passed all specified Graham criteria.")

    # Save all results to a spreadsheet
    save_results_to_spreadsheet(all_results)


if __name__ == "__main__":
    main()
