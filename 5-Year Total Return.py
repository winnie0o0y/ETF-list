import yfinance as yf
import pandas as pd
from datetime import datetime

def compute_total_return(ticker, start_date="2020-01-01"):
    try:
        etf = yf.Ticker(ticker)
        price_df = etf.history(start=start_date)[['Close']].dropna()
        dividends = etf.dividends[etf.dividends.index >= start_date]

        if price_df.empty:
            return {"代碼": ticker, "總報酬率": None}

        shares = 1.0
        cash = 0.0

        for date, dividend in dividends.items():
            if date not in price_df.index:
                continue
            cash += dividend * shares
            new_shares = cash / price_df.loc[date, 'Close']
            shares += new_shares
            cash = 0.0

        start_price = price_df.iloc[0]['Close']
        end_price = price_df.iloc[-1]['Close']
        final_value = shares * end_price
        total_return = final_value / start_price - 1

        return {
            "代碼": ticker,
            "總報酬率 (%)": round(total_return * 100, 2)
        }

    except Exception as e:
        return {"代碼": ticker, "總報酬率 (%)": None, "錯誤": str(e)}

# === ETF 清單 ===
etf_list = ["0050.TW", "0052.TW", "0056.TW", "006208.TW", "00631L.TW",
            "00633L.TW", "00637L.TW", "00646.TW", "00662.TW", "00665L.TW",
            "00670L.TW", "00675L.TW", "00680L.TW", "00688L.TW", "00692.TW",
            "00701.TW",  "00706L.TW", "00711B.TW", "00712.TW", "00713.TW",
            "00715L.TW", "00733.TW", "00752.TW", "00753L.TW", "00757.TW",
            "00770.TW", "00775B.TW", "00830.TW", "00850.TW"]
start_date = "2020-01-01"

# === 執行批次查詢 ===
results = [compute_total_return(ticker, start_date) for ticker in etf_list]
df = pd.DataFrame(results)

# === 顯示結果 ===
pd.set_option('display.float_format', '{:.2f}'.format)
print("台股 ETF 含息總報酬率（2020/01/01 起）：")
print(df)