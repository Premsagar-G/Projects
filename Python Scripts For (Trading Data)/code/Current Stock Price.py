import yfinance as yf
import pandas as pd
from datetime import datetime

# List of stock ticker symbols
stocks = {
    "AARTIIND": "AARTIIND.NS", "ABFRL": "ABFRL.NS", "ACC": "ACC.NS", "ADANIENT": "ADANIENT.NS",
    "Adani Green": "ADANIGREEN.NS", "Adani Power": "ADANIPOWER.NS",
    "Adani Wilmar": "AWL.NS",  "Ambuja Cement": "AMBUJACEM.NS", "Apollo Tyres": "APOLLOTYRE.NS",
    "Ashok Leyland": "ASHOKLEY.NS", "Adani Total Gas": "ATGL.NS", "Axis Bank": "AXISBANK.NS", "Balkrishna Industries": "BALKRISIND.NS",
    "Balrampur Chini": "BALRAMCHIN.NS", "Bandhan Bank": "BANDHANBNK.NS", "Bank of Baroda": "BANKBARODA.NS",
    "BEL": "BEL.NS", "Berger Paints": "BERGEPAINT.NS", "Bharat Forge": "BHARATFORG.NS", "BHEL": "BHEL.NS",
    "BPCL": "BPCL.NS", "Birlasoft": "BSOFT.NS", "CANFINHOME": "CANFINHOME.NS", "Castrol India": "CASTROLIND.NS",
    "Central Bank": "CENTRALBK.NS", "Century Plyboard": "CENTURYPLY.NS", "CESC": "CESC.NS",
    "Chambal Fertilizer": "CHAMBLFERT.NS", "City Union Bank": "CUB.NS", "Coal India": "COALINDIA.NS",
    "Container Corporation": "CONCOR.NS", "Crompton Greaves": "CROMPTON.NS", "Dabur": "DABUR.NS",
    "Delhivery": "DELHIVERY.NS", "DLF": "DLF.NS", "Eicher Motors": "EICHERMOT.NS", "Emami": "EMAMILTD.NS",
    "Exide Industries": "EXIDEIND.NS", "FACT": "FACT.NS", "Federal Bank": "FEDERALBNK.NS",
    "Finolex Industries": "FINPIPE.NS", "GAIL": "GAIL.NS", "GNFC": "GNFC.NS", "Granules India": "GRANULES.NS",
    "Gujarat Gas": "GUJGASLTD.NS", "HINDALCO": "HINDALCO.NS", "HINDCOPPER": "HINDCOPPER.NS",
    "HINDPETRO": "HINDPETRO.NS", "Hindustan Zinc": "HINDZINC.NS", "HUDCO": "HUDCO.NS",
    "ICICI Prudential": "ICICIPRULI.NS", "IDBI": "IDBI.NS", "Vodafone Idea": "IDEA.NS", "IEX": "IEX.NS",
    "IGL": "IGL.NS", "INDHOTEL": "INDHOTEL.NS", "IndusInd Bank": "INDUSINDBK.NS", "Indus Tower": "INDUSTOWER.NS",
    "IOB": "IOB.NS", "IOC": "IOC.NS", "IRCTC": "IRCTC.NS", "IRFC": "IRFC.NS", "Kalyan Jewellers": "KALYANKJIL.NS",
    "Laurus Labs": "LAURUSLABS.NS", "LIC Housing Finance": "LICHSGFIN.NS", "LT Finance": "LTF.NS",
    "M&M Finance": "M&MFIN.NS", "MANAPPURAM": "MANAPPURAM.NS", "Marico": "MARICO.NS", "MGL": "MGL.NS",
    "NATIONALUM": "NATIONALUM.NS", "NCC": "NCC.NS", "NMDC": "NMDC.NS", "NTPC": "NTPC.NS",
    "Oberoi Realty": "OBEROIRLTY.NS", "Ola electric": "OLAELEC.NS", "ONGC": "ONGC.NS", "Petronet LNG": "PETRONET.NS",
    "PFC": "PFC.NS", "Punjab National Bank": "PNB.NS", "POWERGRID": "POWERGRID.NS",
    "Quess Corp": "QUESS.NS", "Rail Vikas Nigam": "RVNL.NS", "RBL Bank": "RBLBANK.NS",
    "REC": "RECLTD.NS", "Reliance": "Reliance.NS", "SAIL": "SAIL.NS", "SBIN": "SBIN.NS",
    "Sun TV": "SUNTV.NS", "Suzlon Energy": "SUZLON.NS", "Swiggy": "SWIGGY.NS", "Tata Motors": "TATAMOTORS.NS",
    "TATAPOWER": "TATAPOWER.NS", "TATASTEEL": "TATASTEEL.NS", "UPL": "UPL.NS", "VEDL": "VEDL.NS",
    "Wipro": "WIPRO.NS", "Yes Bank": "YESBANK.NS", "ETERNAL": "ETERNAL.NS"
}

# Create an empty list to store stock data
stock_data_list = []

# Fetch data for each stock
for stock_name, ticker in stocks.items():
    try:
        print(f"✅Fetching data for {stock_name} ({ticker})...")
        stock_info = yf.Ticker(ticker)
        current_price = stock_info.history(period="1d")["Close"].iloc[-1]  # Get last closing price

        # Append data to list
        stock_data_list.append([stock_name, ticker, current_price])

    except Exception as e:
        print(f"❌Failed to fetch data for {stock_name}: {e}")
        stock_data_list.append([stock_name, ticker, "N/A"])  # Store "N/A" for failed stocks

# Convert list to DataFrame
df = pd.DataFrame(stock_data_list, columns=["Stock", "Ticker", "Current Price"])

# Generate filename with today's date
today_date = datetime.today().strftime("%d-%m-%Y")
file_name = f"current_stock_prices_{today_date}.xlsx"

# Save to Excel file
df.to_excel(file_name, index=False, engine='openpyxl')

print(f"🔥Stock prices saved to {file_name}!")