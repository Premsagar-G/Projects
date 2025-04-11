import requests
import pandas as pd
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# Updated list of companies to fetch option chain data
symbols = [
    "AARTIIND", "ABFRL", "ACC", "ADANIGREEN", "ADANIPOWER", "ATGL", "ADANIWILMAR", "ADANIENT",
    "AMBUJACEM", "APOLLOTYRE", "ASHOKLEY", "AXISBANK", "BALKRISIND", "BALRAMCHIN", "BANDHANBNK", "BANKBARODA",
    "BEL", "BERGEPAINT", "BHARATFORG", "BHEL", "BSOFT", "BPCL", "CANFINHOME", "CASTROLIND", "CENTRALBK",
    "CENTURYPLY", "CESC", "CHAMBLFERT", "CUB", "COALINDIA", "CONCOR", "CROMPTON", "DABUR", "DELHIVERY", "DLF",
    "EICHERMOT", "EMAMILTD", "EXIDEIND", "FACT", "FEDERALBNK", "FINPIPE", "GAIL", "GNFC", "GRANULES", "GUJGASLTD",
    "HINDALCO", "HINDCOPPER", "HINDPETRO", "HINDZINC", "HUDCO", "ICICIPRULI", "IDBI", "IEX", "IGL", "INDHOTEL", "INDUSTOWER",
    "INDUSINDBK", "IOB", "IOC", "IRCTC", "IRFC", "KALYANKJIL", "LAURUSLABS", "LICHSGFIN", "LTF", "M%26MFIN",
    "MANAPPURAM", "MARICO", "MGL", "NATIONALUM", "NCC", "NMDC", "NTPC", "OBEROIRLTY", "OLAELEC", "ONGC", "PETRONET",
    "PFC", "POWERGRID", "PNB", "QUESS", "RVNL", "RBLBANK", "RECLTD", "RELIANCE", "SAIL", "SBIN", "SUNTV", "SUZLON", "SWIGGY",
    "TATAMOTORS", "TATAPOWER", "TATASTEEL", "UPL", "VEDL", "IDEA", "WIPRO", "YESBANK", "ZOMATO", "ETERNAL", 
]

# Common headers for requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json"
}

def get_nse_option_chain(symbol):
    """Fetch option chain data from NSE for a given stock symbol (Optimized for parallel execution)."""
    
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
    
    session = requests.Session()
    try:
        session.get(f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}", headers=HEADERS, timeout=5)
        sleep(random.uniform(1, 3))  # Random delay to reduce detection
        
        response = session.get(url, headers=HEADERS, timeout=5)

        if response.status_code != 200:
            print(f"Failed to fetch data for {symbol}. Status Code:", response.status_code)
            return None

        if "json" not in response.headers.get("Content-Type", ""):
            print(f"Invalid response for {symbol}. Not JSON.")
            return None

        data = response.json()
        records = data.get("records", {}).get("data", [])

        combined_data = []

        for entry in records:
            strike_price = entry.get("strikePrice", 0)
            expiry = entry.get("expiryDate", "NA")
            
            ce = entry.get("CE", {})
            pe = entry.get("PE", {})

            combined_data.append([
                symbol, expiry, strike_price,
                ce.get("bidprice", 0), ce.get("bidQty", 0), ce.get("askPrice", 0), ce.get("askQty", 0),
                pe.get("bidprice", 0), pe.get("bidQty", 0), pe.get("askPrice", 0), pe.get("askQty", 0)
            ])

        return pd.DataFrame(combined_data, columns=[
            "Symbol", "Expiry", "Strike Price",
            "Call Bid Price", "Call Bid Qty", "Call Ask Price", "Call Ask Qty",
            "Put Bid Price", "Put Bid Qty", "Put Ask Price", "Put Ask Qty"
        ])

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {symbol}: {e}")
        return None

# Run multiple requests in parallel
all_data = pd.DataFrame()

with ThreadPoolExecutor(max_workers=10) as executor:  # 10 parallel requests
    future_to_symbol = {executor.submit(get_nse_option_chain, symbol): symbol for symbol in symbols}

    for future in as_completed(future_to_symbol):
        symbol = future_to_symbol[future]
        try:
            df = future.result()
            if df is not None and not df.empty:
                all_data = pd.concat([all_data, df], ignore_index=True)
                print(f"✅Data added for {symbol}!")
            else:
                print(f"⚠️ Skipping {symbol} due to fetch error or no data.")
        except Exception as e:
            print(f"‼️Error processing {symbol}: {e}")

# Save all data to a single CSV file
if not all_data.empty:
    all_data.to_csv("All_Option_Chain_Data.csv", index=False)
    print("🔥All data saved successfully in 'All_Option_Chain_Data.csv'!")
else:
    print("❌No data to save.")
