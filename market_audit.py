import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
from datetime import datetime
import time

def get_audit_metrics(ticker, stock_obj, info):
    """Calculates metrics with improved data mapping for yfinance."""
    try:
        # 1. Fetch Dataframes
        bs = stock_obj.balance_sheet
        is_stmt = stock_obj.financials
        cf = stock_obj.cashflow

        if bs.empty or is_stmt.empty or cf.empty:
            return None

        # Clean and align data
        latest_bs = bs.iloc[:, 0].fillna(0)
        prev_bs = bs.iloc[:, 1].fillna(0) if bs.shape[1] > 1 else latest_bs
        latest_is = is_stmt.iloc[:, 0].fillna(0)
        prev_is = is_stmt.iloc[:, 1].fillna(0) if is_stmt.shape[1] > 1 else latest_is
        latest_cf = cf.iloc[:, 0].fillna(0)

        metrics = {"Ticker": ticker, "Price": info.get('currentPrice', 0)}

        # 2. Net-Net (Graham)
        shares = info.get('sharesOutstanding', 1)
        ncav = latest_bs.get('Total Current Assets', 0) - latest_bs.get('Total Liabilities Net Minority Interest', 0)
        metrics['NCAV_PS'] = ncav / shares if shares else 0

        # 3. Acquirer's Multiple (EV/EBIT)
        ev = info.get('enterpriseValue', 0)
        ebit = latest_is.get('EBIT', latest_is.get('Operating Income', 0))
        metrics['AM_Multiple'] = ev / ebit if ebit > 0 else 999

        # 4. Piotroski F-Score (Robust Check)
        f_score = 0
        f_score += 1 if latest_is.get('Net Income', 0) > 0 else 0
        f_score += 1 if latest_cf.get('Operating Cash Flow', 0) > 0 else 0
        # Compare ROA
        roa_now = latest_is.get('Net Income', 0) / latest_bs.get('Total Assets', 1)
        roa_prev = prev_is.get('Net Income', 0) / prev_bs.get('Total Assets', 1)
        f_score += 1 if roa_now > roa_prev else 0
        # Accrual
        f_score += 1 if latest_cf.get('Operating Cash Flow', 0) > latest_is.get('Net Income', 0) else 0

        metrics['F_Score'] = f_score
        metrics['Dividend_Yield'] = info.get('dividendYield', 0)
        metrics['P_B_Ratio'] = info.get('priceToBook', 999)

        return metrics
    except Exception:
        return None

def run_multi_model_audit():
    print(f"Starting Audit at {datetime.now().strftime('%H:%M:%S')}")

    # Get all tickers
    all_tickers = list(set(si.tickers_nasdaq() + si.tickers_other()))
    results = []

    # Excluded Sectors for Value Models
    excluded_sectors = ['Financial Services', 'Real Estate']

    for i, ticker in enumerate(all_tickers):
        try:
            if not ticker:
                continue

            # Rate limiting: Sleep 1.2 seconds every request to stay under Yahoo's radar
            time.sleep(1.2)

            stock = yf.Ticker(ticker)
            info = stock.info

            # Skip if no info or in excluded sector
            sector = info.get('sector')
            if not sector or sector in excluded_sectors:
                continue

            m = get_audit_metrics(ticker, stock, info)
            if not m: continue

            # DECISION LOGIC
            is_graham = m['Price'] < (m['NCAV_PS'] * 0.66) # 2/3rds of NCAV is the classic rule
            is_acquirer = m['AM_Multiple'] < 10
            is_strong_fscore = m['F_Score'] >= 7
            is_high_dividend = (m['Dividend_Yield'] or 0) > 0.03
            is_low_pb = m['P_B_Ratio'] < 1.2

            if any([is_graham, is_acquirer, is_strong_fscore, is_high_dividend, is_low_pb]):
                m['Graham_Pass'] = "YES" if is_graham else "no"
                m['FScore_Pass'] = "YES" if is_strong_fscore else "no"
                results.append(m)
                print(f"[{i}/{len(all_tickers)}] Match: {ticker} ({sector})")

        except Exception as e:
            print(f"Error on {ticker}: {e}")
            continue

    if results:
        df = pd.DataFrame(results)
        filename = f"Market_Audit_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        df.to_excel(filename, index=False)
        print(f"Audit complete. File saved: {filename}")

run_multi_model_audit()
