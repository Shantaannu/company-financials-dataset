import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("~/Downloads/Financials.csv")

# Function to clean currency-style strings
def clean_currency(val):
    val = str(val)
    val = val.replace('$', '').replace(',', '')
    val = val.strip()
    val = val.replace('(', '-').replace(')', '')
    return val if val not in ['-', ''] else np.nan

# Apply cleaning to all columns
df = df.applymap(clean_currency)

# Convert numeric columns to float
numeric_cols = ["Units Sold", "Manufacturing Price", "Sale Price", "Gross Sales", "Sales", "COGS", "Profit"]
for col in numeric_cols:
    df[col] = df[col].astype(float)

# Reformat the Date column to yyyy-mm-01
df["Date"] = pd.to_datetime(
    df["Year"].astype(str) + "-" +
    df["Month Number"].astype(str).str.zfill(2) + "-01"
)

# Drop unnecessary columns
df.drop(columns=["Month Name", "Month Number", "Year", "Discount Band", "Discounts"], inplace=True)

# Rename financial columns to include "(in $)"
currency_columns = ["Units Sold", "Manufacturing Price", "Sale Price", "Gross Sales", "Sales", "COGS", "Profit"]
df.rename(columns={col: f"{col} (in $)" for col in currency_columns if col in df.columns}, inplace=True)

# Save cleaned and sorted data
df.to_csv("~/Downloads/Cleaned_Financials.csv", index=False)

# Display the cleaned DataFrame
print(df.head())