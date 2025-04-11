import pandas as pd
import httpx
import datetime
from openpyxl import Workbook

# Alpha Vantage API key
API_KEY = "DLOCENHWH72RRJBY"

# Function to fetch historical USDINR spot data using httpx
def fetch_spot_data():
    print("Fetching spot rate data...")
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "FX_DAILY",
        "from_symbol": "USD",
        "to_symbol": "INR",
        "apikey": API_KEY,
        "outputsize": "full"
    }
    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    # Parse data
    if "Time Series FX (Daily)" in data:
        spot_data = data["Time Series FX (Daily)"]
        df = pd.DataFrame.from_dict(spot_data, orient="index")
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close"
        })
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        return df[["Close"]].rename(columns={"Close": "Spot Rate"})
    else:
        raise Exception("Error fetching spot data: ", data)

# Function to compute 3M forward premium in paisa if given as a percentage
def calculate_premium(spot_rate, annualized_premium_percentage):
    return spot_rate * annualized_premium_percentage * (1 / 4) * (1 / 100) * 100

# Combine spot rates and 3M forward premiums
def process_data(spot_df, forward_data):
    print("Processing data...")
    processed_data = []
    for date, row in spot_df.iterrows():
        spot_rate = float(row["Spot Rate"])
        
        # Fetch forward premium (modify this section for actual forward premium source)
        forward_premium_percentage = forward_data.get(date, 0)  # Replace with actual premium data lookup
        premium_paisa = calculate_premium(spot_rate, forward_premium_percentage)
        
        # Calculate forward rate
        forward_rate = spot_rate + (premium_paisa / 100)
        
        # Append data
        processed_data.append({
            "Date": date,
            "Spot Rate": spot_rate,
            "3M Forward Premium (Paisa)": premium_paisa,
            "3M Forward Rate": forward_rate
        })
    
    return pd.DataFrame(processed_data)

# Save the final dataset using openpyxl
def save_to_excel(df, filename="Forex-Historical-Data.xlsx"):
    print(f"Saving data to {filename}...")
    wb = Workbook()
    ws = wb.active
    ws.title = "Forex Data"
    
    # Add headers
    headers = list(df.columns)
    ws.append(headers)
    
    # Add data rows
    for _, row in df.iterrows():
        ws.append(row.tolist())
    
    # Save workbook
    wb.save(filename)
    print("Data saved successfully!")

# Main function
if __name__ == "__main__":
    try:
        # Step 1: Fetch spot data
        spot_df = fetch_spot_data()
        
        # Step 2: Input forward premium data (modify or fetch from your source)
        # Simulating forward premium data as percentages
        start_date = spot_df.index.min()
        end_date = spot_df.index.max()
        date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
        forward_data = {date: 6 if date.month % 3 == 0 else 0 for date in date_range}  # Example: 6% quarterly
        
        # Step 3: Process the data
        processed_df = process_data(spot_df, forward_data)
        
        # Step 4: Save to Excel
        save_to_excel(processed_df, filename="Forex-Historical-Data.xlsx")
        
    except Exception as e:
        print("An error occurred:", e)
